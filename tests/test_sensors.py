import unittest

from smart_home import (
    InvalidValueError,
    MotionSensor,
    Sensor,
    SmokeSensor,
    TemperatureSensor,
)


class TestSensors(unittest.TestCase):
    def test_sensor_is_abstract(self):
        with self.assertRaises(TypeError):
            Sensor("Generic")

    def test_no_value_at_start(self):
        self.assertIsNone(TemperatureSensor("T").value)

    def test_temperature_validation(self):
        sensor = TemperatureSensor("T")
        sensor.record(21.5)
        self.assertEqual(sensor.value, 21.5)
        with self.assertRaises(InvalidValueError):
            sensor.record(500)
        with self.assertRaises(InvalidValueError):
            sensor.record("hot")
        self.assertEqual(sensor.value, 21.5)  # invalid value did not overwrite

    def test_motion_accepts_only_bool(self):
        sensor = MotionSensor("M")
        sensor.record(True)
        self.assertTrue(sensor.value)
        with self.assertRaises(InvalidValueError):
            sensor.record(1)

    def test_smoke_range(self):
        sensor = SmokeSensor("S")
        with self.assertRaises(InvalidValueError):
            sensor.record(120)

    def test_units(self):
        self.assertEqual(TemperatureSensor("T").unit, "°C")
        self.assertEqual(SmokeSensor("S").unit, "%")


if __name__ == "__main__":
    unittest.main()
