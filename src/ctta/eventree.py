#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import os
import logging
from typing import Dict, List, Any


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

_LOGGER = logging.getLogger(__name__)


class TreeItemContainer:
    def __init__(self):
        self.children: List[TreeItem] = []
        self.level = -1

    def get_children(self):
        ret_list = []
        ret_list.extend(self.children)
        for item in self.children:
            ret_list.extend(item.get_children())
        return ret_list

    def set_level(self, new_level):
        self.level = new_level
        for item in self.children:
            item.set_level(new_level + 1)

    def add_item(self, item):
        if not self.children:
            self._append(item)
            return
        self._add_cover(item)
        self._add_side(item)

    def _add_cover(self, item):
        if not self.children:
            return

        # check cover
        item_start = item.start()
        item_end = item.end()

        if item_end < self.children[0].start():
            # before first
            return
        if item_start > self.children[-1].end():
            # after last
            return

        idx = 0
        while idx < len(self.children):
            child = self.children[idx]
            if item_start <= child.start():
                if item_end >= child.end():
                    # fully covers
                    del self.children[idx]
                    item.add_item(child)
                else:
                    if item_end < child.start():
                        break
                    idx += 1
            else:
                idx += 1

    def _add_side(self, item):
        if not self.children:
            self._append(item)
            return

        # add item
        item_start = item.start()
        item_end = item.end()

        if item_end < self.children[0].start():
            # before first
            self._insert(0, item)
            return
        if item_start > self.children[-1].end():
            # after last
            self._append(item)
            return

        for idx, child in enumerate(self.children):
            if item_end <= child.end():
                if item_start >= child.start():
                    # insert inside current item
                    child.add_item(item)
                    return
                if item_end <= child.start():
                    # fully before
                    self._insert(idx, item)
                    return
                # partially before - invalid case
                raise RuntimeError("invalid case")

            if item_start <= child.start():
                # fully covers - case already handled
                raise RuntimeError("invalid case")

            if item_start < child.end():
                # partially after
                raise RuntimeError("invalid case")

            # fully after - continue the loop

        # seems that element is full after
        self._append(item)

    def _insert(self, index, item: "TreeItem"):
        self.children.insert(index, item)
        new_level = self.level + 1
        item.set_level(new_level)

    def _append(self, item: "TreeItem"):
        self.children.append(item)
        new_level = self.level + 1
        item.set_level(new_level)


class TreeItem(TreeItemContainer):
    def __init__(self, event_data):
        super().__init__()
        self.event_data = event_data
        self._start = self.event_data["ts"]
        self._end = self.event_data["ts"] + self.event_data["dur"]

    def __repr__(self) -> str:
        return f"[{id(self)} l: {self.level} s: {self.start()} e: {self.end()}]"

    def start(self):
        return self._start

    def end(self):
        return self._end

    def middle(self):
        return self.event_data["ts"] + float(self.event_data["dur"]) / 2


class EventTree:
    def __init__(self):
        self._container = TreeItemContainer()

    def get_children(self):
        return self._container.get_children()

    def add_event(self, event: Dict[Any, Any]):
        item = TreeItem(event)
        self._container.add_item(item)

    def add_events(self, events_list):
        for event in events_list:
            self.add_event(event)
