"""Devices of the smart home.

`Device` is an abstract base class. It holds everything that is common to
all devices (id, name, power, on/off state). Concrete device types
(Light, Thermostat, Camera, AlarmSystem) inherit from it and add their own
behaviour.
"""

from abc import ABC, abstractmethod

from .exceptions import DeviceOffError, InvalidValueError


class Device(ABC):
    """Abstract base class of every smart home device."""

    # Class attribute: shared by all devices, used to give each one a unique id.
    _id_counter = 0

    def __init__(self, name: str, power_watts: float) -> None:
        if not isinstance(name, str) or not name.strip():
            raise InvalidValueError("Device name cannot be empty.")
        if power_watts < 0:
            raise InvalidValueError("Power consumption cannot be negative.")

        # "Protected" attributes (leading underscore) -> encapsulation.
        self._device_id = Device._generate_id()
        self._name = name.strip()
        self._power_watts = float(power_watts)
        self._is_on = False

    # ------------------------------------------------------------------ #
    # Class method: works on the class itself, not on one object.
    # ------------------------------------------------------------------ #
    @classmethod
    def _generate_id(cls) -> str:
        Device._id_counter += 1
        return f"DEV-{Device._id_counter:03d}"

    # ------------------------------------------------------------------ #
    # Read-only properties (getters without setters)
    # ------------------------------------------------------------------ #
    @property
    def device_id(self) -> str:
        return self._device_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def power_watts(self) -> float:
        """Rated power of the device when it is ON."""
        return self._power_watts

    @property
    def is_on(self) -> bool:
        return self._is_on

    @property
    def current_power(self) -> float:
        """Power the device is consuming right now (0 when OFF)."""
        return self._power_watts if self._is_on else 0.0

    # ------------------------------------------------------------------ #
    # Common behaviour
    # ------------------------------------------------------------------ #
    def turn_on(self) -> None:
        self._is_on = True

    def turn_off(self) -> None:
        self._is_on = False

    def toggle(self) -> None:
        if self._is_on:
            self.turn_off()
        else:
            self.turn_on()

    def _require_on(self, action: str) -> None:
        """Helper used by subclasses: raise an error if the device is OFF."""
        if not self._is_on:
            raise DeviceOffError(f"Cannot {action}: '{self._name}' is OFF.")

    # ------------------------------------------------------------------ #
    # Abstract members: every subclass MUST implement these.
    # ------------------------------------------------------------------ #
    @property
    @abstractmethod
    def device_type(self) -> str:
        """Human readable type name, e.g. 'Light'."""

    @abstractmethod
    def status(self) -> str:
        """Device specific status text, e.g. 'brightness 80%'."""

    # ------------------------------------------------------------------ #
    # Magic (dunder) methods
    # ------------------------------------------------------------------ #
    def __str__(self) -> str:
        state = "ON " if self._is_on else "OFF"
        return f"[{self.device_type:<11}] {self._name:<20} {state} | {self.status()}"

    def __repr__(self) -> str:
        return f"{type(self).__name__}(id={self._device_id!r}, name={self._name!r})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Device) and self._device_id == other._device_id

    def __hash__(self) -> int:
        return hash(self._device_id)


class Light(Device):
    """A dimmable light."""

    def __init__(self, name: str, power_watts: float = 10, brightness: int = 100) -> None:
        super().__init__(name, power_watts)  # call the parent constructor
        self._brightness = 0
        self.brightness = brightness  # goes through the validating setter

    @property
    def device_type(self) -> str:
        return "Light"

    @property
    def brightness(self) -> int:
        return self._brightness

    @brightness.setter
    def brightness(self, value: int) -> None:
        if not 0 <= value <= 100:
            raise InvalidValueError("Brightness must be between 0 and 100.")
        self._brightness = int(value)

    @property
    def current_power(self) -> float:
        # Overridden: a dimmed light uses proportionally less power.
        return super().current_power * self._brightness / 100

    def status(self) -> str:
        return f"brightness {self._brightness}%"


class Thermostat(Device):
    """Controls the heater of a room according to a target temperature."""

    MIN_TEMP = 5.0
    MAX_TEMP = 35.0

    def __init__(self, name: str, power_watts: float = 2000,
                 target_temperature: float = 21.0) -> None:
        super().__init__(name, power_watts)
        self._target_temperature = 0.0
        self.target_temperature = target_temperature
        self._current_temperature = None  # unknown until a sensor reports

    @property
    def device_type(self) -> str:
        return "Thermostat"

    @property
    def target_temperature(self) -> float:
        return self._target_temperature

    @target_temperature.setter
    def target_temperature(self, value: float) -> None:
        if not self.MIN_TEMP <= value <= self.MAX_TEMP:
            raise InvalidValueError(
                f"Target temperature must be between {self.MIN_TEMP} and {self.MAX_TEMP} °C."
            )
        self._target_temperature = float(value)

    @property
    def current_temperature(self):
        return self._current_temperature

    def update_current_temperature(self, value: float) -> None:
        """Called with the latest room temperature (e.g. from a sensor)."""
        self._current_temperature = float(value)

    @property
    def is_heating(self) -> bool:
        """The heater runs only if the thermostat is ON and the room is too cold."""
        return (
            self._is_on
            and self._current_temperature is not None
            and self._current_temperature < self._target_temperature
        )

    @property
    def current_power(self) -> float:
        # Overridden: the thermostat only consumes power while heating.
        return self._power_watts if self.is_heating else 0.0

    def status(self) -> str:
        current = "?" if self._current_temperature is None else f"{self._current_temperature:.1f}"
        heating = "heating" if self.is_heating else "idle"
        return f"target {self._target_temperature:.1f}°C, now {current}°C, {heating}"


class Camera(Device):
    """A security camera that can record."""

    def __init__(self, name: str, power_watts: float = 5) -> None:
        super().__init__(name, power_watts)
        self._is_recording = False

    @property
    def device_type(self) -> str:
        return "Camera"

    @property
    def is_recording(self) -> bool:
        return self._is_recording

    def start_recording(self) -> None:
        self._require_on("start recording")
        self._is_recording = True

    def stop_recording(self) -> None:
        self._is_recording = False

    def turn_off(self) -> None:
        # Overridden: a camera that is switched off also stops recording.
        self.stop_recording()
        super().turn_off()

    def status(self) -> str:
        return "recording" if self._is_recording else "not recording"


class AlarmSystem(Device):
    """A house alarm that can be armed and triggered."""

    def __init__(self, name: str, power_watts: float = 3) -> None:
        super().__init__(name, power_watts)
        self._is_armed = False
        self._is_triggered = False
        self._trigger_reason = None

    @property
    def device_type(self) -> str:
        return "Alarm"

    @property
    def is_armed(self) -> bool:
        return self._is_armed

    @property
    def is_triggered(self) -> bool:
        return self._is_triggered

    @property
    def trigger_reason(self):
        return self._trigger_reason

    def arm(self) -> None:
        self._require_on("arm the alarm")
        self._is_armed = True

    def disarm(self) -> None:
        self._is_armed = False
        self._is_triggered = False
        self._trigger_reason = None

    def trigger(self, reason: str) -> bool:
        """Trigger the alarm. Returns True only if the alarm was armed."""
        if not (self._is_on and self._is_armed):
            return False
        self._is_triggered = True
        self._trigger_reason = reason
        return True

    def turn_off(self) -> None:
        # Overridden: switching the alarm off also disarms it.
        self.disarm()
        super().turn_off()

    def status(self) -> str:
        if self._is_triggered:
            return f"!!! TRIGGERED: {self._trigger_reason}"
        return "armed" if self._is_armed else "disarmed"
