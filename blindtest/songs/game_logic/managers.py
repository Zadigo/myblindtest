import dataclass


@dataclass
class Device:
    device_id: str


class DeviceManager:
    """Class that manages entering and leaving 
    devices in the game e.g. projection devices"""

    def __init__(self):
        self.pending_devices: dict[str, set[str]] = {
            'projectors': set(),
            'buzzers': set()
        }
        self.confirmed_devices: dict[str, set[str]] = {
            'projectors': set(),
            'buzzers': set()
        }

    def __get__(self, instance, cls):
        return self

    def __len__(self):
        return len(self.devices)

    def __iter__(self):
        return iter(self.devices)

    def __getitem__(self, device_id: str):
        return filter(lambda x: x == device_id, self.devices)

    @property
    def pending_devices(self):
        """Devices that are pending confirmation"""
        return self.pending_devices['projectors'].union(self.pending_devices['buzzers'])

    @property
    def confirmed_devices(self):
        """Devices that have been confirmed via a connection token"""
        return self.confirmed_devices['projectors'].union(self.confirmed_devices['buzzers'])

    @property
    def devices(self):
        """All devices that are either pending or confirmed"""
        return self.pending_devices.union(self.confirmed_devices)

    def add_pending_projector(self, device_id: str):
        """Adds this device to the list of pending projectors when
        the device is first connected and no connection token has been 
        received or validated by the admin device"""
        if device_id in self.pending_devices:
            return False

        self.pending_devices['projectors'].add(device_id)
        return True

    def add_pending_buzzer(self, device_id: str):
        """Adds this device to the list of pending buzzers when
        the device is first connected and no connection token has been
        received or validated by the admin device"""
        if device_id in self.pending_devices:
            return False

        self.pending_devices['buzzers'].add(device_id)
        return True

    def add_confirmed_projector(self, device_id: str):
        """Adds this device to the confirmed list of projectors
        if the connection token has been accepted by the admin device"""
        if device_id in self.confirmed_devices:
            return False

        self.pending_devices['projectors'].discard(device_id)
        self.confirmed_devices['projectors'].add(device_id)
        return True

    def add_confirmed_buzzer(self, device_id: str):
        """Adds this device to the confirmed list of buzzers
        if the connection token has been accepted by the admin device"""
        if device_id in self.confirmed_devices:
            return False

        self.pending_devices['buzzers'].discard(device_id)
        self.confirmed_devices['buzzers'].add(device_id)
        return True
