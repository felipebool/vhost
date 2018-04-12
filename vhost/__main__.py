#!/usr/bin/env python3

import argparse
from .action import create_host

def setup_arguments(parser):
    parser.add_argument(
        '-v', '--verbose',
        help='enable output verbosity',
        action='store_true')

    parser.add_argument(
        '-s', '--server',
        help='specify which web server')

    parser.add_argument(
        '-n', '--name',
        help='specify host name')

    parser.add_argument(
        '-u', '--user',
        help='specify ownership for host')

    parser.set_defaults(
        server='apache',
        user='www-data',
    )

def main():
    parser = argparse.ArgumentParser(
        prog='vhost',
        description='Tool for help creating virtual hosts')

    setup_arguments(parser)
    args = parser.parse_args()

    create_host(args)

    print('Please, restart {}'.format(args.server))

if __name__ == '__main__':
    main()

