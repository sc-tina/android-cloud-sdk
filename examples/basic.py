#!/usr/bin/env python3
"""Basic usage of android-cloud-sdk."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.client import CloudDeviceClient

client = CloudDeviceClient()
if client.wait_for_device(timeout=10):
    info = client.device_info()
    print(f"Device: {info.get('model', 'unknown')} (Android {info.get('release', '?')})")
    client.screenshot('example_screen.png')
    pkgs = client.list_packages()
    print(f'Packages: {len(pkgs)}')
