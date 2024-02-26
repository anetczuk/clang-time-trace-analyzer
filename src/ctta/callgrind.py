#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import os
import logging
from typing import List

import pyprof2calltree

# entry fields:
# code -- function name and file location (type string or Code)
# callcount -- number of calls of function
# reccallcount -- ???
# inlinetime -- duration of call itself (without children)
# totaltime -- total duration of call (with children)
# calls -- children calls
from pyprof2calltree import Entry, Code  # pylint: disable=W0611


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

_LOGGER = logging.getLogger(__name__)


class CallgrindConverter(pyprof2calltree.CalltreeConverter):
    pass


# 'top_blocks' can be None (then will not be rendered)
def render(data_entries: List[Entry]):
    converter = CallgrindConverter(data_entries)
    converter.visualize()
