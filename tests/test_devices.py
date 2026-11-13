import unittest

from smart_home import (
    AlarmSystem,
    Camera,
    Device,
    DeviceOffError,
    InvalidValueError,
    Light,
    Thermostat,
)


class TestDeviceBase(unittest.TestCase):
    def test_device_is_abstract(self):
        with self.assertRaises(TypeError):
            Device("Generic", 10)

    def test_ids_are_unique(self):
        a, b = Light("A"), Light("B")
        self.assertNotEqual(a.device_id, b.device_id)
        self.assertNotEqual(a, b)

    def test_empty_name_rejected(self):
        with self.assertRaises(InvalidValueError):
            Light("   ")

    def test_negative_power_rejected(self):
        with self.assertRaises(InvalidValueError):
            Light("Lamp", power_watts=-5)

    def test_toggle(self):
        lamp = Light("Lamp")
        lamp.toggle()
        self.assertTrue(lamp.is_on)
        lamp.toggle()
        self.assertFalse(lamp.is_on)

    def test_read_only_property(self):
        lamp = Light("Lamp")
        with self.assertRaises(AttributeError):
            lamp.is_on = True


class TestLight(unittest.TestCase):
    def test_brightness_validation(self):
        lamp = Light("Lamp")
        with self.assertRaises(InvalidValueError):
            lamp.brightness = 101
        with self.assertRaises(InvalidValueError):
            Light("Lamp", brightness=-1)

    def test_power_depends_on_brightness(self):
        lamp = Light("Lamp", power_watts=60, brightness=50)
        self.assertEqual(lamp.current_power, 0)
        lamp.turn_on()
        self.assertEqual(lamp.current_power, 30)


class TestThermostat(unittest.TestCase):
    def test_target_range(self):
        with self.assertRaises(InvalidValueError):
            Thermostat("T", target_temperature=50)

    def test_heats_only_when_on_and_cold(self):
        t = Thermostat("T", power_watts=2000, target_temperature=21)
        t.update_current_temperature(18)
        self.assertFalse(t.is_heating)          # OFF
        t.turn_on()
        self.assertTrue(t.is_heating)           # ON and cold
        self.assertEqual(t.current_power, 2000)
        t.update_current_temperature(23)
        self.assertFalse(t.is_heating)          # warm enough
        self.assertEqual(t.current_power, 0)


class TestCamera(unittest.TestCase):
    def test_cannot_record_when_off(self):
        with self.assertRaises(DeviceOffError):
            Camera("Cam").start_recording()

    def test_turn_off_stops_recording(self):
        cam = Camera("Cam")
        cam.turn_on()
        cam.start_recording()
        cam.turn_off()
        self.assertFalse(cam.is_recording)


class TestAlarmSystem(unittest.TestCase):
    def test_trigger_requires_armed(self):
        alarm = AlarmSystem("Alarm")
        alarm.turn_on()
        self.assertFalse(alarm.trigger("motion"))
        alarm.arm()
        self.assertTrue(alarm.trigger("motion"))
        self.assertEqual(alarm.trigger_reason, "motion")

    def test_cannot_arm_when_off(self):
        with self.assertRaises(DeviceOffError):
            AlarmSystem("Alarm").arm()

    def test_turn_off_disarms(self):
        alarm = AlarmSystem("Alarm")
        alarm.turn_on()
        alarm.arm()
        alarm.trigger("smoke")
        alarm.turn_off()
        self.assertFalse(alarm.is_armed)
        self.assertFalse(alarm.is_triggered)


class TestPolymorphism(unittest.TestCase):
    def test_every_device_has_own_status(self):
        devices = [Light("L"), Thermostat("T"), Camera("C"), AlarmSystem("A")]
        types = {d.device_type for d in devices}
        self.assertEqual(types, {"Light", "Thermostat", "Camera", "Alarm"})
        for device in devices:
            self.assertIsInstance(device, Device)
            self.assertIsInstance(device.status(), str)


if __name__ == "__main__":
    unittest.main()
