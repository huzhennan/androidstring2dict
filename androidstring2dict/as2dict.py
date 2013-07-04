#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import sys
from commands import InitCommand, GenerateCommand, ExportCommand, ImportCommand

COMMANDS = {
    'init': InitCommand,
    'generate': GenerateCommand,
    'export': ExportCommand,
    'import': ImportCommand,
}

def parse_args(args):
    from . import get_version
    parser = argparse.ArgumentParser(add_help=True,
                                     description="Add android component's string resource to a dictionary."
                                                 "else can import and export. After updatd dictionary, we else"
                                                 "can generate new .po file",
                                     epilog='Written by: zhennan.hu')
    parser.add_argument('--version', action='version', version=get_version())


    subparsers = parser.add_subparsers(dest="command", title='commands',
                                       description='valid commands',
                                       help='additional help')

    for name, cmdclass in COMMANDS.items():
        cmd_parser = subparsers.add_parser(name, add_help=True)
        group = cmd_parser.add_argument_group('command arguments')
        cmdclass.setup_arg_parser(group)


    return parser.parse_args(args[1:])

def main(argv):
    options = parse_args(argv)
    print options

    cmd = COMMANDS[options.command](options)
    cmd.execute()


