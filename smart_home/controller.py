"""The controller is the "brain" that the user talks to.

It does not store devices itself; it works on a House that is given to it
from outside (dependency injection). It only depends on the abstract
`Device` / `Sensor` contracts, so new device types can be added later
without changing this class.
"""

from .devices import Device, Thermostat
from .exceptions import DeviceNotFoundError
from .house import House
from .sensors import TemperatureSensor


class Controller:
    """Central control unit of a smart home."""

    def __init__(self, house: House) -> None:
        self._house = house  # association: the controller *uses* a house

    @property
    def house(self) -> House:
        return self._house

    # ---- finding devices -------------------------------------------------
    def find_device(self, device_id: str) -> Device:
        for device in self._house.all_devices:
            if device.device_id == device_id:
                return device
        raise DeviceNotFoundError(f"No device with id {device_id}.")

    def find_devices_by_name(self, text: str) -> list[Device]:
        text = text.lower()
        return [d for d in self._house.all_devices if text in d.name.lower()]

    def devices_of_type(self, device_class: type) -> list[Device]:
        return [d for d in self._house.all_devices if isinstance(d, device_class)]

    # ---- switching -------------------------------------------------------
    def turn_on_room(self, room_name: str) -> None:
        for device in self._house.get_room(room_name):
            device.turn_on()

    def turn_off_room(self, room_name: str) -> None:
        for device in self._house.get_room(room_name):
            device.turn_off()

    def turn_off_all(self) -> None:
        for device in self._house.all_devices:
            device.turn_off()

    # ---- sensors -> devices ---------------------------------------------
    def update_thermostats(self) -> None:
        """Send the temperature of each room to the thermostats of that room."""
        for room in self._house:
            readings = [s.value for s in room.sensors_of_type(TemperatureSensor)
                        if s.value is not None]
            if not readings:
                continue
            average = sum(readings) / len(readings)
            for thermostat in room.devices_of_type(Thermostat):
                thermostat.update_current_temperature(average)

    # ---- reporting -------------------------------------------------------
    def status_report(self) -> str:
        lines = [f"=== {self._house} ==="]
        for room in self._house:
            lines.append(f"\n{room}")
            for device in room:
                # Polymorphism: str(device) calls the status() of the real subclass.
                lines.append(f"   {device}")
            for sensor in room.sensors:
                lines.append(f"   {sensor}")
        return "\n".join(lines)
