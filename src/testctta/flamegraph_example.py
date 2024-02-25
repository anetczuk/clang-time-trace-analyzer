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

from ctta.flamegraph import render, BlockItem


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

_LOGGER = logging.getLogger(__name__)


def main():
    blocks = None
    bblocks = [
        BlockItem(0, 100, 0, 0, "xxx_full", "xxx_short", "xxx_hash"),
        {"level": 2, "x": 50, "w": 100, "color": 0, "hash_name": "xxx2", "name": "xxx2", "full_name": "xxx2"},
    ]

    render(blocks, bblocks, "/tmp/xxx_flame.svg")


if __name__ == "__main__":
    main()
