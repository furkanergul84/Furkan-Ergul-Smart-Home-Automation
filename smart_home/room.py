"""A room groups the devices and sensors that are physically inside it."""

from .devices import Device
from .exceptions import DeviceNotFoundError, DuplicateError, InvalidValueError
from .sensors import Sensor


class Room:
    """A room of the house.

    Relationship: *aggregation* - devices and sensors are created outside
    the room and only placed into it. They can be removed and still exist.
    """

    def __init__(self, name: str) -> None:
        if not isinstance(name, str) or not name.strip():
            raise InvalidValueError("Room name cannot be empty.")
        self._name = name.strip()
        # Internal collections are private: other classes use methods instead.
        self._devices: dict[str, Device] = {}
        self._sensors: dict[str, Sensor] = {}

    @property
    def name(self) -> str:
        return self._name

    # ---- devices ---------------------------------------------------------
    def add_device(self, device: Device) -> None:
        if not isinstance(device, Device):
            raise InvalidValueError("Only Device objects can be added to a room.")
        if device.device_id in self._devices:
            raise DuplicateError(f"'{device.name}' is already in {self._name}.")
        self._devices[device.device_id] = device

    def remove_device(self, device_id: str) -> Device:
        try:
            return self._devices.pop(device_id)
        except KeyError:
            raise DeviceNotFoundError(f"No device {device_id} in {self._name}.") from None

    def get_device(self, device_id: str) -> Device:
        try:
            return self._devices[device_id]
        except KeyError:
            raise DeviceNotFoundError(f"No device {device_id} in {self._name}.") from None

    @property
    def devices(self) -> tuple[Device, ...]:
        """A read-only copy, so outside code cannot change the room's list."""
        return tuple(self._devices.values())

    def devices_of_type(self, device_class: type) -> list[Device]:
        """E.g. room.devices_of_type(Light) -> all lights in this room."""
        return [d for d in self._devices.values() if isinstance(d, device_class)]

    # ---- sensors ---------------------------------------------------------
    def add_sensor(self, sensor: Sensor) -> None:
        if not isinstance(sensor, Sensor):
            raise InvalidValueError("Only Sensor objects can be added to a room.")
        if sensor.sensor_id in self._sensors:
            raise DuplicateError(f"'{sensor.name}' is already in {self._name}.")
        self._sensors[sensor.sensor_id] = sensor

    def remove_sensor(self, sensor_id: str) -> Sensor:
        try:
            return self._sensors.pop(sensor_id)
        except KeyError:
            raise DeviceNotFoundError(f"No sensor {sensor_id} in {self._name}.") from None

    @property
    def sensors(self) -> tuple[Sensor, ...]:
        return tuple(self._sensors.values())

    def sensors_of_type(self, sensor_class: type) -> list[Sensor]:
        return [s for s in self._sensors.values() if isinstance(s, sensor_class)]

    # ---- calculations ----------------------------------------------------
    @property
    def current_power(self) -> float:
        # Polymorphism: each device computes its own power in its own way.
        return sum(device.current_power for device in self._devices.values())

    # ---- magic methods ---------------------------------------------------
    def __len__(self) -> int:
        return len(self._devices)

    def __contains__(self, item) -> bool:
        if isinstance(item, Device):
            return item.device_id in self._devices
        if isinstance(item, Sensor):
            return item.sensor_id in self._sensors
        return False

    def __iter__(self):
        return iter(self._devices.values())

    def __str__(self) -> str:
        devices, sensors = len(self._devices), len(self._sensors)
        return (f"Room '{self._name}' ({devices} device{'s' if devices != 1 else ''}, "
                f"{sensors} sensor{'s' if sensors != 1 else ''}, {self.current_power:.1f} W)")

    def __repr__(self) -> str:
        return f"Room(name={self._name!r})"
