import dataclasses
import datetime
from dataclasses import field

import pytz


@dataclasses.dataclass
class Device:
    """Dataclass representing a device. A device
    can be either a projector (projecting screen) or
    a buzzer (smartphone used by the user to buzz)
    in order to give an answer to a song to guess"""

    device_id: str
    confirmed: bool = False
    is_projector: bool = False
    is_buzzer: bool = False
    created_on: datetime.datetime = field(
        default_factory=datetime.datetime.now)

    def __post_init__(self):
        self.created_on = self.created_on.replace(tzinfo=pytz.UTC)

    def __repr__(self):
        return f'Device(id={self.device_id}, confirmed={self.confirmed})'

    def __eq__(self, other):
        if not isinstance(other, Device):
            return NotImplemented
        return self.device_id == other.device_id

    def __hash__(self):
        return hash(self.device_id)


class DeviceManager:
    """Class that manages entering and leaving 
    devices in the game e.g. projection devices"""

    def __init__(self):
        self.devices: set[Device] = set()
        self.connection_token: str | None = None

    def __get__(self, instance, cls):
        self.connection_token = getattr(instance, 'connection_token', None)
        return self

    def __len__(self):
        return len(self.devices)

    def __iter__(self):
        return iter(self.devices)

    def __getitem__(self, device_id: str):
        return list(filter(lambda x: x.device_id == device_id, self.devices))

    def __repr__(self):
        return f'DeviceManager(devices={list(self.devices)})'

    @property
    def pending_devices(self):
        """Devices that are pending confirmation"""
        return filter(lambda x: not x.confirmed, self.devices)

    @property
    def confirmed_devices(self):
        """Devices that have been confirmed via a connection token"""
        return filter(lambda x: x.confirmed, self.devices)

    def add_pending_projector(self, device_id: str):
        """Adds this device to the list of pending projectors when
        the device is first connected and no connection token has been 
        received or validated by the admin device"""
        if device_id in self.devices:
            return False

        self.devices.add(Device(device_id=device_id, is_projector=True))

    def add_pending_buzzer(self, device_id: str):
        """Adds this device to the list of pending buzzers when
        the device is first connected and no connection token has been
        received or validated by the admin device"""
        if device_id in self.devices:
            return False

        self.devices.add(Device(device_id=device_id, is_buzzer=True))
        return True

    def confirm_device(self, device_id: str):
        """Adds a pending device to the confirmed list of devices
        if the connection token has been accepted by the admin device"""
        for device in self.devices:
            if device.device_id == device_id and not device.confirmed:
                device.confirmed = True
                return True
        return False

    def remove(self, device_id: str):
        """Removes a device from the list of devices"""
        for device in self.devices:
            if device.device_id == device_id:
                self.devices.remove(device)
                return True
        return False
