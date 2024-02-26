#!/usr/bin/env python3

#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import sys
import os
import logging
import argparse

import pprint

from glob import glob

# from ctta.analyzer import draw_flame_svg
from ctta.analyzer import analyze, run_callgrind_view, draw_flame_svg


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

_LOGGER = logging.getLogger(__name__)


# =============================================================


def process_analyze(args):
    files_list = find_files(args.files, args.dirs)
    excludes = args.exclude
    out_file_path = args.outfile
    _LOGGER.info("parsing files: %s", files_list)
    data_dict = analyze(files_list, excludes)

    pprint.pprint(data_dict, indent=4, sort_dicts=False)

    with open(out_file_path, "w", encoding="utf-8") as out_file:
        pprint.pprint(data_dict, out_file, indent=4, sort_dicts=False)


def process_flamegraph(args):
    data_file = args.file
    out_svg_path = args.outfile
    _LOGGER.info("parsing file: %s", data_file)
    draw_flame_svg(data_file, out_svg_path)


def process_flamegraphs(args):
    files_list = find_files(args.files, args.dirs)
    files_len = len(files_list)
    for idx, file_path in enumerate(files_list):
        _LOGGER.info("%s/%s: drawing flamegraph of %s", idx, files_len, file_path)
        out_svg_path = f"{file_path}.svg"
        draw_flame_svg(file_path, out_svg_path)


def process_callgrind(args):
    files_list = find_files(args.files, args.dirs)
    out_callgrind_path = args.outfile
    run_callgrind_view(files_list, out_callgrind_path)


# =============================================================


def analyze_code(files_list, exclude_list, out_file_path):
    data_dict = analyze(files_list, exclude_list)

    pprint.pprint(data_dict, indent=4, sort_dicts=False)

    with open(out_file_path, "w", encoding="utf-8") as out_file:
        pprint.pprint(data_dict, out_file, indent=4, sort_dicts=False)


def find_files(files, dirs):
    ret_list = set()
    ret_list.update(files)

    for dir_item in dirs:
        for found_json in glob(f"{dir_item}/**/*.json", recursive=True):
            ret_list.add(found_json)

    ret_list = sorted(ret_list)
    return ret_list


# =============================================================


def main():
    parser = argparse.ArgumentParser(description="clang-time-trace-analyzer")
    parser.add_argument("--listtools", action="store_true", help="List tools")
    parser.set_defaults(func=None)

    subparsers = parser.add_subparsers(help="one of tools", description="use one of tools", dest="tool", required=False)

    ## =================================================

    description = "perform simple analysis of JSON files"
    subparser = subparsers.add_parser("analyze", help=description)
    subparser.description = description
    subparser.set_defaults(func=process_analyze)
    subparser.add_argument("-la", "--logall", action="store_true", help="Log all messages")
    subparser.add_argument("-f", "--files", nargs="+", default=[], help="Files to analyze")
    subparser.add_argument(
        "-d", "--dirs", nargs="+", default=[], help="Directories to analyze (will recursively search for JSON files)"
    )
    subparser.add_argument(
        "--exclude", nargs="+", default=[], help="Space separated list of items to exclude. e.g. '/usr/*'"
    )
    subparser.add_argument("--outfile", action="store", required=False, help="Path to output file")

    ## =================================================

    description = "draw JSON file as flame graph"
    subparser = subparsers.add_parser("flamegraph", help=description)
    subparser.description = description
    subparser.set_defaults(func=process_flamegraph)
    subparser.add_argument("-la", "--logall", action="store_true", help="Log all messages")
    subparser.add_argument("-f", "--file", action="store", required=True, help="JSON file to analyze")
    subparser.add_argument("--outfile", action="store", required=True, help="Path to output file")

    ## =================================================

    description = "draw JSON files as flame graphs next to given JSONs"
    subparser = subparsers.add_parser("flamegraphs", help=description)
    subparser.description = description
    subparser.set_defaults(func=process_flamegraphs)
    subparser.add_argument("-la", "--logall", action="store_true", help="Log all messages")
    subparser.add_argument("-f", "--files", nargs="+", default=[], help="Files to analyze")
    subparser.add_argument(
        "-d", "--dirs", nargs="+", default=[], help="Directories to analyze (will recursively search for JSON files)"
    )

    ## =================================================

    description = "display JSON files in kcachegrind viewer"
    subparser = subparsers.add_parser("callgrind", help=description)
    subparser.description = description
    subparser.set_defaults(func=process_callgrind)
    subparser.add_argument("-la", "--logall", action="store_true", help="Log all messages")
    subparser.add_argument("-f", "--files", nargs="+", default=[], help="Files to analyze")
    subparser.add_argument(
        "-d", "--dirs", nargs="+", default=[], help="Directories to analyze (will recursively search for JSON files)"
    )
    subparser.add_argument("--outfile", action="store", required=False, help="Path to output file")

    ## =================================================

    args = parser.parse_args()

    # logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)

    if args.listtools is True:
        tools_list = list(subparsers.choices.keys())
        print(", ".join(tools_list))
        return 0

    if not args.func:
        ## no command given -- print help message
        parser.print_help()
        sys.exit(1)
        return 1

    args.func(args)

    _LOGGER.info("Completed")
    return 0


## ============================= main section ===================================


if __name__ == "__main__":
    EXIT_CODE = main()
    sys.exit(EXIT_CODE)
