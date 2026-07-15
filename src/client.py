"""CloudDeviceClient - Python SDK for cloud Android devices."""
import logging, os, subprocess, time

log = logging.getLogger(__name__)

class CloudDeviceClient:
    def __init__(self, device_serial=None, adb_path='adb'):
        self.device_serial = device_serial
        self._adb_base = [adb_path]
        if device_serial:
            self._adb_base += ['-s', device_serial]

    def _run(self, args, timeout=30):
        try:
            r = subprocess.run(self._adb_base + args, capture_output=True, text=True, timeout=timeout)
            return r.stdout.strip(), r.stderr.strip(), r.returncode
        except subprocess.TimeoutExpired:
            return '', 'TIMEOUT', -1

    def device_info(self):
        props = ['ro.product.model', 'ro.product.manufacturer', 'ro.build.version.release',
                 'ro.build.version.sdk', 'ro.serialno']
        result = {}
        for p in props:
            out, _, _ = self._run(['shell', 'getprop', p])
            result[p.split('.')[-1]] = out.strip() or 'unknown'
        return result

    def screenshot(self, output=None):
        remote = '/sdcard/screen.png'
        self._run(['shell', 'screencap', '-p', remote])
        output = output or f'screen_{int(time.time())}.png'
        out, err, rc = self._run(['pull', remote, output], timeout=15)
        self._run(['shell', 'rm', remote])
        return output if rc == 0 and os.path.exists(output) else None

    def shell(self, command):
        return self._run(['shell', command], timeout=60)

    def install_apk(self, apk_path):
        if not os.path.exists(apk_path):
            return False
        out, err, rc = self._run(['install', '-r', apk_path], timeout=120)
        return rc == 0 and ('Success' in out)

    def push(self, local, remote='/sdcard/'):
        if not os.path.exists(local):
            return False
        _, _, rc = self._run(['push', local, remote], timeout=30)
        return rc == 0

    def pull(self, remote, local):
        _, _, rc = self._run(['pull', remote, local], timeout=30)
        return rc == 0

    def input_tap(self, x, y):
        return self._run(['shell', 'input', 'tap', str(x), str(y)])[2] == 0

    def input_text(self, text):
        return self._run(['shell', 'input', 'text', text.replace(' ', '%s')])[2] == 0

    def input_swipe(self, x1, y1, x2, y2, duration=300):
        return self._run(['shell', 'input', 'swipe', str(x1), str(y1), str(x2), str(y2), str(duration)])[2] == 0

    def list_packages(self):
        out, _, rc = self._run(['shell', 'pm', 'list', 'packages', '-3'])
        return [p.replace('package:', '') for p in out.split() if p.startswith('package:')]

    def is_online(self):
        out, _, rc = self._run(['get-state'])
        return rc == 0 and 'device' in out

    def wait_for_device(self, timeout=60):
        start = time.time()
        while time.time() - start < timeout:
            if self.is_online():
                return True
            time.sleep(2)
        return False
