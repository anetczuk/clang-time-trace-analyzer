#!/usr/bin/env python3
#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import unittest

from ctta.eventree import EventTree


class EventTreeMock(EventTree):
    def add_simple(self, start, end):
        event = {"ts": start, "dur": end - start}
        self.add_event(event)


class EventTreeTest(unittest.TestCase):
    def test_add_event_first(self):
        tree = EventTreeMock()
        tree.add_event({"ts": 100, "dur": 100})

        items_list = tree.get_children()
        self.assertEqual(len(items_list), 1)
        self.assertEqual(items_list[0].middle(), 150.0)
        self.assertEqual(items_list[0].level, 0)

    def test_add_event_before(self):
        tree = EventTreeMock()
        tree.add_event({"ts": 100, "dur": 100})
        tree.add_event({"ts": 10, "dur": 10})

        items_list = tree.get_children()
        self.assertEqual(len(items_list), 2)
        self.assertEqual(items_list[0].middle(), 15.0)
        self.assertEqual(items_list[0].level, 0)
        self.assertEqual(items_list[1].middle(), 150.0)
        self.assertEqual(items_list[1].level, 0)

    def test_add_event_after(self):
        tree = EventTreeMock()
        tree.add_event({"ts": 100, "dur": 100})
        tree.add_event({"ts": 300, "dur": 100})

        items_list = tree.get_children()
        self.assertEqual(len(items_list), 2)
        self.assertEqual(items_list[0].middle(), 150.0)
        self.assertEqual(items_list[0].level, 0)
        self.assertEqual(items_list[1].middle(), 350.0)
        self.assertEqual(items_list[1].level, 0)

    def test_add_event_inside(self):
        tree = EventTreeMock()
        tree.add_event({"ts": 100, "dur": 100})
        tree.add_event({"ts": 160, "dur": 20})

        items_list = tree.get_children()
        self.assertEqual(len(items_list), 2)
        self.assertEqual(items_list[0].middle(), 150.0)
        self.assertEqual(items_list[0].level, 0)
        self.assertEqual(items_list[1].middle(), 170.0)
        self.assertEqual(items_list[1].level, 1)

    def test_add_event_cover(self):
        tree = EventTreeMock()
        tree.add_event({"ts": 100, "dur": 100})
        tree.add_event({"ts": 80, "dur": 200})

        items_list = tree.get_children()
        self.assertEqual(len(items_list), 2)
        self.assertEqual(items_list[0].middle(), 180.0)
        self.assertEqual(items_list[0].level, 0)
        self.assertEqual(items_list[1].middle(), 150.0)
        self.assertEqual(items_list[1].level, 1)

    def test_add_event_cover2(self):
        tree = EventTreeMock()
        tree.add_event({"ts": 100, "dur": 100})
        tree.add_event({"ts": 80, "dur": 200})
        tree.add_event({"ts": 50, "dur": 300})

        items_list = tree.get_children()
        self.assertEqual(len(items_list), 3)
        self.assertEqual(items_list[0].middle(), 200.0)
        self.assertEqual(items_list[0].level, 0)
        self.assertEqual(items_list[1].middle(), 180.0)
        self.assertEqual(items_list[1].level, 1)
        self.assertEqual(items_list[2].middle(), 150.0)
        self.assertEqual(items_list[2].level, 2)

    def test_add_event_cover3(self):
        tree = EventTreeMock()
        tree.add_simple(100, 200)
        tree.add_simple(300, 400)
        tree.add_simple(50, 450)

        items_list = tree.get_children()
        self.assertEqual(len(items_list), 3)
        self.assertEqual(items_list[0].middle(), 250.0)
        self.assertEqual(items_list[0].level, 0)
        self.assertEqual(items_list[1].middle(), 150.0)
        self.assertEqual(items_list[1].level, 1)
        self.assertEqual(items_list[2].middle(), 350.0)
        self.assertEqual(items_list[2].level, 1)
