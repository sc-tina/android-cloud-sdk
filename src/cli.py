#!/usr/bin/env python3
"""CloudDeviceClient CLI."""
import argparse, json
from .client import CloudDeviceClient

def main():
    parser = argparse.ArgumentParser(description='Cloud Android SDK CLI')
    parser.add_argument('--device', '-d', default='')
    sub = parser.add_subparsers(dest='command')
    sub.add_parser('info')
    sub.add_parser('online')
    sub.add_parser('packages')
    ss = sub.add_parser('screenshot')
    ss.add_argument('-o', '--output', default='screen.png')
    inst = sub.add_parser('install')
    inst.add_argument('apk_path')
    tap = sub.add_parser('tap')
    tap.add_argument('x', type=int)
    tap.add_argument('y', type=int)
    shell = sub.add_parser('shell')
    shell.add_argument('command', nargs='+')
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    client = CloudDeviceClient(device_serial=args.device) if args.device else CloudDeviceClient()
    if args.command == 'info':
        print(json.dumps(client.device_info(), indent=2))
    elif args.command == 'online':
        print(f'Online: {client.is_online()}')
    elif args.command == 'screenshot':
        p = client.screenshot(args.output)
        print(f'Screenshot: {p}' if p else 'Failed')
    elif args.command == 'install':
        print('OK' if client.install_apk(args.apk_path) else 'FAIL')
    elif args.command == 'tap':
        print('OK' if client.input_tap(args.x, args.y) else 'FAIL')
    elif args.command == 'packages':
        for p in client.list_packages():
            print(f'  {p}')
    elif args.command == 'shell':
        out, err, rc = client.shell(' '.join(args.command))
        print(out)

if __name__ == '__main__':
    main()
