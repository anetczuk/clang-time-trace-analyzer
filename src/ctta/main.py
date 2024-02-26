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
from ctta.analyzer import analyze, run_callgrind_view


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

_LOGGER = logging.getLogger(__name__)


def analyze_code(files_list, exclude_list, out_file_path):
    data_dict = analyze(files_list, exclude_list)

    pprint.pprint(data_dict, indent=4, sort_dicts=False)

    with open(out_file_path, "w", encoding="utf-8") as out_file:
        pprint.pprint(data_dict, out_file, indent=4, sort_dicts=False)

    # out_svg_path = f"{out_file_path}.svg"
    # draw_flame_svg(files_list, out_svg_path)

    run_callgrind_view(files_list)


def find_files(files, dirs):
    ret_list = set()
    ret_list.update(files)

    for dir_item in dirs:
        for found_json in glob(f"{dir_item}/**/*.json", recursive=True):
            ret_list.add(found_json)

    ret_list = sorted(ret_list)
    return ret_list


def main():
    parser = argparse.ArgumentParser(description="clang-time-trace-analyzer")
    parser.add_argument("-f", "--files", nargs="+", default=[], help="Files to analyze")
    parser.add_argument("-d", "--dirs", nargs="+", default=[], help="Directories to analyze")
    parser.add_argument(
        "--exclude", nargs="+", default=[], help="Space separated list of items to exclude. e.g. '/usr/*'"
    )
    parser.add_argument("--outfile", action="store", required=False, help="Path to output file")

    args = parser.parse_args()

    # logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)

    files_list = find_files(args.files, args.dirs)
    _LOGGER.info("parsing files: %s", files_list)

    analyze_code(files_list, args.exclude, args.outfile)

    _LOGGER.info("done")
    return 0


## ============================= main section ===================================


if __name__ == "__main__":
    EXIT_CODE = main()
    sys.exit(EXIT_CODE)
