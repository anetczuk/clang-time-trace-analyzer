#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import os
import logging
from dataclasses import dataclass

import re
import json

from ctta.flamegraph import render, BlockItem


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

_LOGGER = logging.getLogger(__name__)


def analyze(files_list, exclude_list):
    exclude_filter = ExcludeItemFilter(exclude_list)
    _LOGGER.info("exclude list: %s", exclude_filter.raw_exclude)

    merged_dict = {}
    for data_path in files_list:
        events_list = read_events(data_path)
        if not events_list:
            continue

        for event in events_list:
            ev_name = event.get("name")
            if ev_name != "Source":
                continue
            event_data = get_data(event)
            if not event_data:
                continue
            if exclude_filter.excluded(event_data["file"]):
                continue
            add_data(merged_dict, event_data)

    # merged_dict = {k: v for k, v in sorted(merged_dict.items(), key=lambda item: item[1])}
    merged_dict = dict(sorted(merged_dict.items(), key=lambda item: item[1].avg()))
    return merged_dict


@dataclass
class Data:
    # file: str = None
    dur: int = 0  # duration given in microseconds (10^-6 s)
    count: int = 0

    def avg(self):
        return float(self.dur) / self.count


def add_data(merged_dict, event_data):
    file = event_data["file"]
    item_data = merged_dict.get(file, None)
    if item_data is None:
        item_data = Data()
        # item_data.file = file
    item_data.dur += event_data["dur"]
    item_data.count += 1
    merged_dict[file] = item_data


def get_data(event):
    args = event.get("args", {})
    if not args:
        return {}
    detail = args.get("detail", "")
    detail = os.path.normpath(detail)
    dur = event.get("dur", 0)
    return {"dur": dur, "file": detail}


##
class ExcludeItemFilter:
    def __init__(self, exclude_set=None):
        self.raw_exclude = set(exclude_set)
        if self.raw_exclude is None:
            self.raw_exclude = set()
        for item in self.raw_exclude.copy():
            if len(item) < 1:
                self.raw_exclude.remove(item)

        self.exclude_set = set()
        self.regex_set = set()

        for excl in self.raw_exclude:
            if "*" in excl:
                ## wildcard found
                pattern = excl
                pattern = pattern.replace("*", ".*")
                regex_obj = re.compile(pattern)
                self.regex_set.add(regex_obj)
            else:
                self.exclude_set.add(excl)

    ## is item excluded?
    def excluded(self, item):
        if item in self.exclude_set:
            return True
        for regex in self.regex_set:
            if regex.match(item):
                return True
        return False


# =============================================================================


def draw_flame_svg(files_list, out_svg_path):
    data_file = files_list[0]
    blocks, bblocks = read_flame_blocks(data_file)
    render(blocks, bblocks, out_svg_path)


def read_flame_blocks(data_file_path):
    top_blocks = []
    bottom_blocks = []

    events_list = read_events(data_file_path)
    if not events_list:
        _LOGGER.warning("unable to get trace events from file: %s", data_file_path)
        return top_blocks, bottom_blocks

    for event in events_list:
        if event["ph"] != "X":
            continue

        item = BlockItem()
        item.x = event["ts"]
        item.w = event["dur"]

        args = event.get("args", {})
        event_name = args.get("detail")
        if event_name is None:
            event_name = event.get("name")

        item.name = os.path.basename(event_name)
        item.full_name = event_name
        item.hash_name = event_name

        if event["tid"] < 1:
            top_blocks.append(item)
        else:
            item.color = 1
            bottom_blocks.append(item)

    top_blocks.sort(key=lambda item: item.x)
    bottom_blocks.sort(key=lambda item: item.x)

    fill_block_level(top_blocks)
    fill_block_level(bottom_blocks)

    return top_blocks, bottom_blocks


def fill_block_level(blocks_list):
    for block in blocks_list:
        middle = block.middle()
        pointed_blocks = get_blocks(blocks_list, middle)
        level = pointed_blocks.index(block)
        block.level = level


def get_blocks(blocks_list, pos):
    ret_list = []
    for item in blocks_list:
        if item.is_in_block(pos):
            ret_list.append(item)
        if pos < item.x:
            break
    return ret_list


# event fields:
# 'pid' -- process id
# 'tid' -- thread id (each chart is in separate row)
# 'ph' -- 'X' or 'M'
# 'cat' -- only for 'M' item
# 'ts' -- 'time start' (in microseconds)
# 'dur' -- 'duration' (in microseconds)
# 'name' -- label on item
# 'args' -- dict with 'detail' and 'count' items
def read_events(trace_file_path):
    try:
        with open(trace_file_path, encoding="utf-8") as data_file:
            dict_data = json.load(data_file)
            if not isinstance(dict_data, dict):
                return None
            events_list = dict_data.get("traceEvents")
            if not events_list:
                return None
            return events_list

    except json.decoder.JSONDecodeError:
        return None
