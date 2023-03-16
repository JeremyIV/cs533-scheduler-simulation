import bisect
from collections import namedtuple

Event = namedtuple("Event", ["type", "job_id"])


def find_event(event_list, event_type=None, job_id=None, get_last=False):
    assert (event_type is not None) or (
        job_id is not None
    ), "must specify either an event type or job id!"
    indices = range(len(event_list))
    if get_last:
        indices = reversed(indices)
    for index in indices:
        time, event = event_list[index]
        event_type_matches = event_type is None or event_type == event.type
        job_id_matches = job_id is None or job_id == event.job_id
        if event_type_matches and job_id_matches:
            return index
    return None


class EventQueue:
    """
    A priority queue of events, where events are popped off in the order that they occur based on their scheduled time.

    Attributes:
        queue (list): The list representing the priority queue of events.

    Methods:
        push(event: Event, time: float) -> None:
            Add an event to the priority queue at a specified time.

        pop_next_event() -> Event:
            Remove and return the next event in the priority queue.

        get_next_event_time() -> Union[float, None]:
            Get the time of the next event in the priority queue.

        get_event(event_type: Optional[str]=None, job_id: Optional[int]=None, get_last: bool=False) -> Union[Event, None]:
            Get the specified event from the priority queue based on its event type and/or job id.

        remove_event(event_type: Optional[str]=None, job_id: Optional[int]=None, get_last: bool=False) -> None:
            Remove the specified event from the priority queue based on its event type and/or job id.
    """

    def __init__(self):
        """
        Initialize an empty priority queue of events.
        """
        self.queue = []

    def push(self, event, time):
        """
        Add an event to the priority queue at a specified time.

        Args:
            event (namedtuple): The event to be added to the priority queue.
            time (float): The time at which the event is scheduled to occur.

        Returns:
            None.
        """

        bisect.insort_left(self.queue, (time, event))

    def pop_next_event(self):
        """
        Remove and return the next event in the priority queue.

        Returns:
            The next event in the priority queue.
        """
        time, event = self.queue.pop(0)
        return event

    def get_next_event_time(self):
        """
        Get the time of the next event in the priority queue.

        Returns:
            The time of the next event in the priority queue, or None if the priority queue is empty.
        """
        if self.queue:
            time, _ = self.queue[0]
            return time
        else:
            return None

    def _find_event(self, event_type=None, job_id=None, get_last=False):
        """
        Find the index of the specified event in the priority queue based on its event type and/or job id.

        Args:
            event_type (str, optional): The type of the event to find.
            job_id (int, optional): The job ID of the event to find.
            get_last (bool, optional): Whether to find the last event in the priority queue that matches the specified criteria.

        Returns:
            The index of the specified event in the priority queue, or None if the event is not found.
        """

        assert (event_type is not None) or (
            job_id is not None
        ), "must specify either an event type or job id!"
        indices = range(len(self.queue))
        if get_last:
            indices = reversed(indices)
        for index in indices:
            time, event = self.queue[index]
            event_type_matches = event_type is None or event_type == event.type
            job_id_matches = job_id is None or job_id == event.job_id
            if event_type_matches and job_id_matches:
                return index
        return None

    def get_event(self, event_type=None, job_id=None, get_last=False):
        """
        Get the specified event from the priority queue based on its event type and/or job id.

        Args:
            event_type (str, optional): The type of the event to get.
            job_id (int, optional): The job ID of the event to get.
            get_last (bool, optional): Whether to get the last event in the priority queue that matches the specified criteria.

        Returns:
            The specified event from the priority queue, or None if the event is not found.
        """

        event_index = find_event(self.queue, event_type, job_id, get_last)
        if event_index is None:
            return None, None
        else:
            return self.queue[event_index]

    def remove_event(self, event_type=None, job_id=None, get_last=False):
        """
        Remove the specified event from the priority queue based on its event type and/or job id.

        Args:
            event_type (str, optional): The type of the event to remove.
            job_id (int, optional): The job ID of the event to remove.
            get_last (bool, optional): Whether to remove the last event in the priority queue that matches the specified criteria.

        Returns:
            None.
        """

        event_index = find_event(self.queue, event_type, job_id, get_last)
        if event_index is not None:
            del self.queue[event_index]

    def __bool__(self):
        return bool(self.queue)
