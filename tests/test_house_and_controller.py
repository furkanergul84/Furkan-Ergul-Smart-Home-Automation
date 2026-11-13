import unittest

from smart_home import (
    Camera,
    Controller,
    DeviceNotFoundError,
    DuplicateError,
    House,
    Light,
    TemperatureSensor,
    Thermostat,
)


class TestRoom(unittest.TestCase):
    def setUp(self):
        self.house = House("Test House")
        self.room = self.house.add_room("Kitchen")
        self.lamp = Light("Kitchen Lamp", power_watts=20)

    def test_add_and_remove_device(self):
        self.room.add_device(self.lamp)
        self.assertIn(self.lamp, self.room)
        self.assertEqual(len(self.room), 1)
        removed = self.room.remove_device(self.lamp.device_id)
        self.assertIs(removed, self.lamp)       # aggregation: device still exists
        self.assertNotIn(self.lamp, self.room)

    def test_duplicate_device(self):
        self.room.add_device(self.lamp)
        with self.assertRaises(DuplicateError):
            self.room.add_device(self.lamp)

    def test_devices_is_a_copy(self):
        self.room.add_device(self.lamp)
        self.assertIsInstance(self.room.devices, tuple)

    def test_room_power(self):
        self.room.add_device(self.lamp)
        self.lamp.turn_on()
        self.assertEqual(self.room.current_power, 20)


class TestHouse(unittest.TestCase):
    def test_house_creates_rooms(self):
        house = House("H")
        room = house.add_room("Bedroom")
        self.assertIs(house.get_room("bedroom"), room)  # case-insensitive lookup
        with self.assertRaises(DuplicateError):
            house.add_room("BEDROOM")

    def test_missing_room(self):
        with self.assertRaises(DeviceNotFoundError):
            House("H").get_room("Garage")

    def test_find_room_of_device(self):
        house = House("H")
        room = house.add_room("Hall")
        cam = Camera("Cam")
        room.add_device(cam)
        self.assertIs(house.find_room_of(cam), room)


class TestController(unittest.TestCase):
    def setUp(self):
        self.house = House("H")
        self.living = self.house.add_room("Living")
        self.lamp = Light("Living Lamp", power_watts=50)
        self.thermostat = Thermostat("Living Thermostat", target_temperature=22)
        self.sensor = TemperatureSensor("Living Temp")
        self.living.add_device(self.lamp)
        self.living.add_device(self.thermostat)
        self.living.add_sensor(self.sensor)
        self.controller = Controller(self.house)

    def test_turn_on_and_off_room(self):
        self.controller.turn_on_room("Living")
        self.assertTrue(self.lamp.is_on and self.thermostat.is_on)
        self.controller.turn_off_all()
        self.assertFalse(self.lamp.is_on or self.thermostat.is_on)

    def test_find_device(self):
        self.assertIs(self.controller.find_device(self.lamp.device_id), self.lamp)
        with self.assertRaises(DeviceNotFoundError):
            self.controller.find_device("DEV-999")
        self.assertEqual(self.controller.find_devices_by_name("lamp"), [self.lamp])

    def test_update_thermostats_from_sensor(self):
        self.sensor.record(18)
        self.controller.update_thermostats()
        self.assertEqual(self.thermostat.current_temperature, 18)
        self.thermostat.turn_on()
        self.assertTrue(self.thermostat.is_heating)

    def test_status_report_lists_everything(self):
        report = self.controller.status_report()
        for name in ("Living Lamp", "Living Thermostat", "Living Temp"):
            self.assertIn(name, report)


if __name__ == "__main__":
    unittest.main()
