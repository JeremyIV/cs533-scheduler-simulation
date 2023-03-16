# TODO
# add three events in every possible order
# assert that the next event time is always the earliest
# assert the the events are popped in the correct order

# add two events which happen at the same time
# assure events still occur in order.
# Doesn't matter which order events at the same time happen in though.

# add a bunch of events to the queue
# test that get_event works with a job id and no event type
# check that it works with an event type and no job id
# test that get_event works with get_last = True, get_last=False

# check remove_event under the same conditions.

import unittest
from datetime import datetime, timedelta
from unittest.mock import patch
from typing import List
from itertools import permutations

from event_queue import Event, EventQueue


class TestEventQueue(unittest.TestCase):
    def setUp(self):
        self.event_queue = EventQueue()

    def test_push_pop_single_event(self):
        # Test that we can push a single event and pop it off the queue
        event = Event("job_started", 1)
        time = datetime.now()
        self.event_queue.push(event, time)
        self.assertEqual(self.event_queue.pop_next_event(), event)

    def test_push_pop_multiple_events(self):
        # Test that we can push multiple events and pop them off the queue in the correct order
        events = [
            Event("job_started", 1),
            Event("job_completed", 1),
            Event("job_started", 2),
            Event("job_completed", 2),
        ]
        times = [datetime.now() + timedelta(seconds=i) for i in range(len(events))]
        events_and_times = list(zip(events, times))
        # no matter what order the events are inserted in, they come out in chronological order.
        for insertion_permutation in permutations(events_and_times):
            for event, time in insertion_permutation:
                self.event_queue.push(event, time)
            for event in events:
                self.assertEqual(self.event_queue.pop_next_event(), event)

    def test_get_next_event_time(self):
        # Test that we can get the time of the next event
        event = Event("job_started", 1)
        time = datetime.now()
        self.assertIsNone(self.event_queue.get_next_event_time())
        self.event_queue.push(event, time)
        self.assertEqual(self.event_queue.get_next_event_time(), time)

    def test_get_event(self):
        # Test that we can get the correct event from the queue
        events = [
            Event("job_started", 1),
            Event("job_completed", 1),
            Event("job_started", 2),
            Event("job_completed", 2),
        ]
        times = [datetime.now() + timedelta(seconds=i) for i in range(len(events))]
        for event, time in zip(events, times):
            self.event_queue.push(event, time)
        self.assertEqual(
            self.event_queue.get_event(event_type="job_started"), (times[0], events[0])
        )
        self.assertEqual(self.event_queue.get_event(job_id=2), (times[2], events[2]))
        self.assertEqual(
            self.event_queue.get_event(event_type="job_started", job_id=3), (None, None)
        )

    def test_remove_event(self):
        # Test that we can remove the correct event from the queue
        events = [
            Event("job_started", 1),
            Event("job_completed", 1),
            Event("job_started", 2),
            Event("job_completed", 2),
        ]
        times = [datetime.now() + timedelta(seconds=i) for i in range(len(events))]

        for event, time in zip(events, times):
            self.event_queue.push(event, time)
        self.event_queue.remove_event(event_type="job_started", job_id=2)
        self.assertEqual(
            self.event_queue.get_event(event_type="job_started", job_id=2), (None, None)
        )
