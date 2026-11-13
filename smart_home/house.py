"""The house is the top level container of the model."""

from .devices import Device
from .exceptions import DeviceNotFoundError, DuplicateError, InvalidValueError
from .room import Room


class House:
    """A house made of rooms.

    Relationship: *composition* - the house itself creates its rooms
    (`add_room` takes a name, not a Room object). A room cannot exist
    without its house.
    """

    def __init__(self, name: str) -> None:
        if not isinstance(name, str) or not name.strip():
            raise InvalidValueError("House name cannot be empty.")
        self._name = name.strip()
        self._rooms: dict[str, Room] = {}

    @property
    def name(self) -> str:
        return self._name

    def add_room(self, room_name: str) -> Room:
        """Create a new room inside the house and return it."""
        key = room_name.strip().lower()
        if key in self._rooms:
            raise DuplicateError(f"Room '{room_name}' already exists.")
        room = Room(room_name)
        self._rooms[key] = room
        return room

    def remove_room(self, room_name: str) -> None:
        if self._rooms.pop(room_name.strip().lower(), None) is None:
            raise DeviceNotFoundError(f"No room called '{room_name}'.")

    def get_room(self, room_name: str) -> Room:
        try:
            return self._rooms[room_name.strip().lower()]
        except KeyError:
            raise DeviceNotFoundError(f"No room called '{room_name}'.") from None

    @property
    def rooms(self) -> tuple[Room, ...]:
        return tuple(self._rooms.values())

    @property
    def all_devices(self) -> list[Device]:
        return [device for room in self._rooms.values() for device in room.devices]

    def find_room_of(self, device: Device) -> Room:
        """Return the room in which `device` is placed."""
        for room in self._rooms.values():
            if device in room:
                return room
        raise DeviceNotFoundError(f"'{device.name}' is not in any room.")

    @property
    def current_power(self) -> float:
        return sum(room.current_power for room in self._rooms.values())

    def __len__(self) -> int:
        return len(self._rooms)

    def __iter__(self):
        return iter(self._rooms.values())

    def __str__(self) -> str:
        return f"House '{self._name}' ({len(self._rooms)} rooms, {self.current_power:.1f} W)"

    def __repr__(self) -> str:
        return f"House(name={self._name!r})"
