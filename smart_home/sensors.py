"""Sensors of the smart home.

A sensor only *measures* something; it does not act. `Sensor` is an
abstract base class; each concrete sensor decides which values are valid
and in which unit they are measured.
"""

from abc import ABC, abstractmethod

from .exceptions import InvalidValueError


class Sensor(ABC):
    """Abstract base class of every sensor."""

    _id_counter = 0

    def __init__(self, name: str) -> None:
        if not isinstance(name, str) or not name.strip():
            raise InvalidValueError("Sensor name cannot be empty.")
        Sensor._id_counter += 1
        self._sensor_id = f"SEN-{Sensor._id_counter:03d}"
        self._name = name.strip()
        self._value = None  # last measured value, None = no reading yet

    @property
    def sensor_id(self) -> str:
        return self._sensor_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self):
        return self._value

    def record(self, value) -> None:
        """Store a new reading after it has been validated by the subclass."""
        self._validate(value)
        self._value = value

    # ---- abstract members ----------------------------------------------
    @property
    @abstractmethod
    def unit(self) -> str:
        """Unit of the measured value, e.g. '°C'."""

    @abstractmethod
    def _validate(self, value) -> None:
        """Raise InvalidValueError if `value` is not a valid reading."""

    # ---- representation --------------------------------------------------
    def __str__(self) -> str:
        shown = "no data" if self._value is None else f"{self._value}{self.unit}"
        return f"<{type(self).__name__}> {self._name}: {shown}"

    def __repr__(self) -> str:
        return f"{type(self).__name__}(id={self._sensor_id!r}, name={self._name!r})"


class TemperatureSensor(Sensor):
    """Measures air temperature in °C."""

    MIN_VALUE = -50.0
    MAX_VALUE = 100.0

    @property
    def unit(self) -> str:
        return "°C"

    def _validate(self, value) -> None:
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise InvalidValueError("Temperature must be a number.")
        if not self.MIN_VALUE <= value <= self.MAX_VALUE:
            raise InvalidValueError(
                f"Temperature must be between {self.MIN_VALUE} and {self.MAX_VALUE} °C."
            )


class MotionSensor(Sensor):
    """Detects movement: True = motion detected, False = no motion."""

    @property
    def unit(self) -> str:
        return ""

    def _validate(self, value) -> None:
        if not isinstance(value, bool):
            raise InvalidValueError("Motion value must be True or False.")


class SmokeSensor(Sensor):
    """Measures smoke density as a percentage (0-100)."""

    @property
    def unit(self) -> str:
        return "%"

    def _validate(self, value) -> None:
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise InvalidValueError("Smoke level must be a number.")
        if not 0 <= value <= 100:
            raise InvalidValueError("Smoke level must be between 0 and 100.")
