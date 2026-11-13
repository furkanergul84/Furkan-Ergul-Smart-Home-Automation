"""Smart Home Automation System - Stage 1 (architecture)."""

from .controller import Controller
from .devices import AlarmSystem, Camera, Device, Light, Thermostat
from .exceptions import (
    DeviceNotFoundError,
    DeviceOffError,
    DuplicateError,
    InvalidValueError,
    SmartHomeError,
)
from .house import House
from .room import Room
from .sensors import MotionSensor, Sensor, SmokeSensor, TemperatureSensor

__all__ = [
    "Controller",
    "Device", "Light", "Thermostat", "Camera", "AlarmSystem",
    "Sensor", "TemperatureSensor", "MotionSensor", "SmokeSensor",
    "Room", "House",
    "SmartHomeError", "InvalidValueError", "DeviceOffError",
    "DeviceNotFoundError", "DuplicateError",
]
