#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import os
import pathlib
import textwrap

import settings

resolutions = [16, 32, 64, 128, 256, 512]
formats = ["1.13", "1.15"]


class CLIFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass


def cli():
    parser = argparse.ArgumentParser(
        prog="phantom",
        description="a tool to convert Minecraft resource packs from 1.8-1.12 to 1.13 or 1.15",
        epilog=textwrap.dedent("""\
        MIT License
        
        Copyright (c) 2018 icrdr
        Copyright (c) 2019 MamiyaOtaru
        Copyright (c) 2020 trevorwarnerOIT 
        Copyright (c) 2021 DeflatedPickle
        
        https://github.com/DeflatedPickle/phantom
        """),
        formatter_class=CLIFormatter
    )

    # log_level = parser.add_mutually_exclusive_group()
    # log_level.add_argument("-v", "--verbose", action="store_true", help="change the logging verbosity")
    # log_level.add_argument("-q", "--quiet", action="store_true", help="change the logging verbosity")

    parser.add_argument("pack", help="the pack location")
    parser.add_argument("res", type=int, choices=resolutions, help="the resolution of the pack")

    parser.add_argument("-n", "--name", nargs='?',
                        help="the file name of the converted pack")
    parser.add_argument("-s", "--suffix", nargs='?',
                        help="an extra string to add to the end of the converted pack name")

    parser.add_argument("-d", "--destination", nargs='?',
                        help="the directory the converted pack will be placed in (if none uses pack directory)")

    parser.add_argument("-f", "--format", choices=formats, default=formats[-1],
                        help="the game version to convert to")

    parser.add_argument("--boxcraft", action="store_true",
                        help="toggles the BoxCraft texture fix")

    return parser.parse_args()


if __name__ == "__main__":
    args = cli()

    settings.game_format = args.format

    from main import main

    main(
        pack=args.pack,
        destination=pathlib.Path(args.pack).parent if not args.destination else os.path.expandvars(args.destination),
        resolution=args.res,
        new_name=args.name,
        name_suffix=args.suffix or "",
        tex=args.boxcraft
    )
