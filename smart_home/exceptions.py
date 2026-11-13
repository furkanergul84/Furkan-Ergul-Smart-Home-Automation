"""Custom exceptions of the Smart Home system.

All exceptions inherit from SmartHomeError, so a caller can catch every
error of this package with a single `except SmartHomeError`.
"""


class SmartHomeError(Exception):
    """Base class for all Smart Home errors."""


class InvalidValueError(SmartHomeError, ValueError):
    """Raised when a value is outside of its allowed range (e.g. brightness 150%)."""


class DeviceOffError(SmartHomeError):
    """Raised when an operation needs the device to be ON but it is OFF."""


class DeviceNotFoundError(SmartHomeError):
    """Raised when a device / sensor / room cannot be found."""


class DuplicateError(SmartHomeError):
    """Raised when the same device / sensor / room is added twice."""
