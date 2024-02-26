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

from ctta.eventree import EventTree
from ctta.flamegraph import BlockItem
from ctta.flamegraph import render as render_flamegraph
from ctta.callgrind import render as render_callgrind
from ctta.callgrind import Entry


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


def draw_flame_svg(file_path, out_svg_path):
    blocks, bblocks = read_flame_blocks(file_path)
    if not blocks and not bblocks:
        return
    render_flamegraph(blocks, bblocks, out_svg_path)


def read_flame_blocks(data_file_path):
    events_list = read_events(data_file_path)
    if not events_list:
        _LOGGER.warning("unable to get trace events from file: %s", data_file_path)
        return [], []

    top_event_tree = EventTree()
    bottom_event_tree = EventTree()

    for event in events_list:
        if event["ph"] != "X":
            continue
        if event["tid"] < 1:
            top_event_tree.add_event(event)
        else:
            bottom_event_tree.add_event(event)

    top_blocks = get_blocks_from_tree(top_event_tree, 0)
    bottom_blocks = get_blocks_from_tree(bottom_event_tree, 1)

    if not bottom_blocks:
        return bottom_blocks, top_blocks
    return top_blocks, bottom_blocks


def get_blocks_from_tree(event_tree, color):
    blocks_list = []

    top_items = event_tree.get_children()
    for item in top_items:
        event = item.event_data

        block = BlockItem()
        block.x = event["ts"]
        block.w = event["dur"]
        block.level = item.level
        block.color = color

        args = event.get("args", {})
        event_name = args.get("detail")
        if event_name is None:
            event_name = event.get("name")

        block.name = os.path.basename(event_name)
        block.full_name = event_name
        block.hash_name = event_name

        blocks_list.append(block)

    return blocks_list


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


# =============================================================================


def run_callgrind_view(files_list):
    data_entries = []
    files_len = len(files_list)
    for idx, data_file in enumerate(files_list):
        _LOGGER.info("%s/%s: drawing callgrind view for %s", idx, files_len, data_file)
        entries = read_callgrind_enries(data_file)
        data_entries.extend(entries)
    render_callgrind(data_entries)


def read_callgrind_enries(data_file_path):
    events_list = read_events(data_file_path)
    if not events_list:
        _LOGGER.warning("unable to get trace events from file: %s", data_file_path)
        return []

    top_event_tree = EventTree()
    bottom_event_tree = EventTree()

    for event in events_list:
        if event["ph"] != "X":
            continue
        if event["tid"] < 1:
            top_event_tree.add_event(event)
        else:
            bottom_event_tree.add_event(event)

    top_entries = get_entries_from_tree(top_event_tree, data_file_path)
    return top_entries


def get_entries_from_tree(event_tree, data_file_path):
    entries_list = []
    entries_dict = {}

    top_items = event_tree.get_children()
    for item in top_items:
        entry = entries_dict.get(item)
        if entry is None:
            entry = get_entry_from_item(item, data_file_path)
            entries_dict[item] = entry
            entries_list.append(entry)

        for child_item in item.children:
            child_entry = entries_dict.get(child_item)
            if child_entry is None:
                child_entry = get_entry_from_item(child_item, data_file_path)
                entries_dict[child_item] = child_entry
                entries_list.append(child_entry)
            entry.calls.append(child_entry)

    return entries_list


def get_entry_from_item(item, data_file_path):
    event = item.event_data

    args = event.get("args", {})
    event_name = args.get("detail")
    if event_name is None:
        event_name = event.get("name")

    if event_name == "ExecuteCompiler":
        event_name = data_file_path
    elif event_name in ["Frontend", "Backend", "CodeGenPasses", "PerformPendingInstantiations", "PerModulePasses"]:
        event_name = f"{data_file_path}:{event_name}"

    # short_name = os.path.basename(event_name)
    # code = Code(event_name, 0, short_name)
    code = event_name

    children_dur = 0
    for child in item.children:
        child_event = child.event_data
        children_dur += float(child_event["dur"])

    duration = float(event["dur"]) / 1000000  # convert to seconds
    children_dur = float(children_dur) / 1000000  # convert to seconds
    self_dur = duration - children_dur
    entry = Entry(code, 1, 1, self_dur, duration, [])

    return entry
