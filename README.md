# android-cloud-sdk

Python SDK for managing cloud Android devices via ADB. Screenshot, APK install, input simulation, file transfer, and multi-device pool.

## Features
- Screenshot capture
- APK install/uninstall
- Touch/keyboard/gesture input
- File push/pull
- Device property inspection
- Multi-device connection pool
- CLI interface

## Quick Start
```bash
pip install -e .
python -c "from src.client import CloudDeviceClient; print('OK')"
```

## CLI
```bash
python -m src.cli info
python -m src.cli screenshot -o screen.png
python -m src.cli install app.apk
```

## Contact
- Website: https://www.qtphone.com/
