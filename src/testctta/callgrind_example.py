#!/usr/bin/env python3
#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

try:
    ## following import success only when file is directly executed from command line
    ## otherwise will throw exception when executing as parameter for "python -m"
    # pylint: disable=W0611
    import __init__
except ImportError:
    ## when import fails then it means that the script was executed indirectly
    ## in this case __init__ is already loaded
    pass

import os
import logging

from ctta.callgrind import render, Entry, Code


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

_LOGGER = logging.getLogger(__name__)


def main():
    en01 = Entry(Code("/aaa/bbb/xxx_full_path.cpp", 11, "xxx_short"), 3, 7, 33, 77, [])
    en02 = Entry(Code("yyy_full_path", 12, "yyy_short"), 4, 8, 34, 78, [])
    en03 = Entry(Code("zzz_full_path", 13, "zzz_short"), 5, 9, 35, 79, [])
    en04 = Entry(Code("zzz_full_path", 13, "zzz_short"), 6, 10, 36, 80, [])

    en01.calls.append(en02)
    en01.calls.append(en03)
    en02.calls.append(en04)

    entries = []
    entries.append(en01)
    entries.append(en02)
    entries.append(en03)
    entries.append(en04)
    render(entries)


if __name__ == "__main__":
    main()
