"""CloudDevicePool - connection pool for multiple devices."""
from .client import CloudDeviceClient
import threading

class CloudDevicePool:
    def __init__(self, max_workers=5):
        self._devices = {}
        self._lock = threading.Lock()

    def add_device(self, serial):
        with self._lock:
            if serial not in self._devices:
                self._devices[serial] = CloudDeviceClient(device_serial=serial)

    def remove_device(self, serial):
        with self._lock:
            self._devices.pop(serial, None)

    def get_device(self, serial):
        with self._lock:
            return self._devices.get(serial)

    def broadcast(self, method, *args, **kwargs):
        results = {}
        with self._lock:
            devices = dict(self._devices)
        for serial, client in devices.items():
            try:
                fn = getattr(client, method)
                results[serial] = fn(*args, **kwargs)
            except Exception as e:
                results[serial] = f'error: {e}'
        return results

    def online_devices(self):
        results = []
        with self._lock:
            items = list(self._devices.items())
        for serial, client in items:
            if client.is_online():
                results.append((serial, client))
        return results

    @property
    def count(self):
        with self._lock:
            return len(self._devices)
