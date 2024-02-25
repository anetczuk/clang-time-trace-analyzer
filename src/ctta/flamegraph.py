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
from dataclasses import dataclass

import flameprof


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

_LOGGER = logging.getLogger(__name__)


@dataclass
class BlockItem:
    x: int = 0  # offset from left edge
    w: int = 0  # width of item on graph scaled to 'maxw'
    level: int = 0  # 0 level is placed on top of image
    color: int = 0  # color palette (level value decreases color intensity)
    name: str = ""  # presented on image
    full_name: str = ""  # presented as tooltip
    hash_name: str = ""  # for fill color

    def __getitem__(self, key):
        if not hasattr(self, key):
            raise RuntimeError(f"no attribute: {key}")
        return getattr(self, key)

    def left(self):
        return self.x

    def right(self):
        return self.x + self.w

    def middle(self):
        return self.x + float(self.w) / 2

    def is_in_block(self, pos):
        pos_dif = pos - self.x
        if pos_dif < 0:
            return False
        return pos_dif <= self.w


# 'top_blocks' can be None (then will not be rendered)
def render(top_blocks: List[BlockItem], bottom_blocks: List[BlockItem], out_file_path: str):
    top_width = calc_max_width(top_blocks)
    bottom_width = calc_max_width(bottom_blocks)
    maxw = max(top_width, bottom_width, 100)

    with open(out_file_path, "w", encoding="utf-8") as out_file:
        svg_content = flameprof.render_svg(top_blocks, bottom_blocks, maxw)
        out_file.write(svg_content)


def calc_max_width(blocks):
    if not blocks:
        return 0
    ret_width = 0
    for item in blocks:
        width = item["x"] + item["w"]
        ret_width = max(ret_width, width)
    return ret_width
