from event_queue import EventQueue, Event
from job import Job, Task, COMPUTE, MEMORY, DISK, NETWORK

# This simulation code is becoming a bit of a mess. Think about it more systematically.
# What comprises the state of our system?

# - remaining tasks for each job
# - which job is currently on the CPU
# - whether the CPU is still context switching to the new job
# - Whether a job is blocked

START_JOB = "START_JOB"
SWITCHING_DONE = "SWITCHING_DONE"
COMPUTING_DONE = "COMPUTING_DONE"
MEMORY_DONE = "MEMORY_DONE"
DISK_DONE = "DISK_DONE"
NETWORK_DONE = "NETWORK_DONE"

WAITING_DONE_TYPES = {MEMORY_DONE, DISK_DONE, NETWORK_DONE}
import pdb


class Simulation:
    def __init__(self, job_timeline, schedule_every=10, context_switch_time=2):
        """
        args:
        job_timeline: list (start_time, job): jobs do not need IDs set; the simulation will assign job ids.
        """
        self.job_timeline = job_timeline
        self.schedule_every = schedule_every
        self.context_switch_time = context_switch_time
        self.need_scheduling = False
        self.events = EventQueue()
        self.history = []
        self.jobs = {}
        self.current_job = None
        self.time = 0

        for job_id, job_start in enumerate(job_timeline):
            start_time, job = job_start
            job.id = job_id
            self.events.push(Event(START_JOB, job_id), start_time)

        self.context_switching = False

    def run_until_scheduling_needed(self):
        assert not self.need_scheduling
        # pdb.set_trace()
        while not (self.is_finished() or self.need_scheduling):
            self._process_next_events()

    def schedule_job(self, job_id):
        """
        Schedules the given job,
        then updates the simulation
        to the next time step where the scheduler
        needs to make another decision.
        """
        # if this is the id of the job that's already on the CPU, nothing changes
        assert self.need_scheduling
        current_job_id = None if self.current_job is None else self.current_job.id

        if current_job_id != job_id:
            # We're de-scheduling the current job. Remove any events which assume
            # it is scheduled on the CPU.
            if current_job_id is not None:
                self.events.remove_event(
                    event_type=SWITCHING_DONE, job_id=current_job_id
                )
                self.events.remove_event(
                    event_type=COMPUTING_DONE, job_id=current_job_id
                )

            # schedule the new job
            self.current_job = self.jobs[job_id]
            self.context_switching = True

            # add event for switching_done
            switching_done_time = self.time + self.context_switch_time
            event = Event(SWITCHING_DONE, job_id)
            self.events.push(event, switching_done_time)

        self.need_scheduling = False

    def _process_next_events(self):

        assert self.need_scheduling == False
        next_event_time = self.events.get_next_event_time()
        if next_event_time is None:
            assert not self.jobs
        time_elapsed = next_event_time - self.time
        self.time = next_event_time

        # If the current job is running, reduce its remaining compute time.
        if self.current_job is not None and self.current_job.remaining_tasks:
            current_task = self.current_job.remaining_tasks[0]
            task_type, time_remaining = current_task
            is_computing = (
                not self.context_switching
                and not self.current_job.blocked
                and task_type == COMPUTE
            )
            if is_computing:
                new_time_remaining = time_remaining - time_elapsed
                self.current_job.remaining_tasks[0] = Task(COMPUTE, new_time_remaining)

        # Process all the events which occur at this time.
        while self.events.get_next_event_time() == self.time:
            event = self.events.pop_next_event()
            self._process_event(event)
            self.history.append((self.time, event))

    def _process_event(self, event):
        event_type, job_id = event
        is_current_job = self.current_job is not None and job_id == self.current_job.id
        if event_type == START_JOB:
            start_time, job = self.job_timeline[job_id]
            assert self.time == start_time
            self.jobs[job_id] = job
            self.need_scheduling = True
        elif event_type == SWITCHING_DONE:
            assert is_current_job
            self.context_switching = False
        elif event_type in WAITING_DONE_TYPES:
            self.jobs[job_id].blocked = False
            self.need_scheduling = bool(self.jobs)
        elif event_type == COMPUTING_DONE:
            assert is_current_job
            self.need_scheduling = bool(self.jobs)

        # if event_type == "COMPUTING_DONE" and self.time == 7:
        # pdb.set_trace()

        if (
            is_current_job
            and not self.context_switching
            and not self.current_job.blocked
        ):
            self._start_next_task(self.current_job)

    def _start_next_task(self, job):
        # if there's no next task, then the job is done!
        assert job.id == self.current_job.id
        if not job.remaining_tasks:
            # job is finished!
            self.current_job = None
            del self.jobs[job.id]
            self.need_scheduling = bool(self.jobs)
            return

        task_type, time_remaining = job.remaining_tasks.pop(0)

        if task_type == COMPUTE:
            event = Event(type=COMPUTING_DONE, job_id=job.id)
            time = self.time + time_remaining
            self.events.push(event, time)
            return
        for io_task_type, io_done_type in {
            (MEMORY, MEMORY_DONE),
            (DISK, DISK_DONE),
            (NETWORK, NETWORK_DONE),
        }:
            if task_type == io_task_type:
                last_event_time, last_event = self.events.get_event(
                    event_type=io_done_type, get_last=True
                )
                if last_event_time is None:
                    last_event_time = self.time
                event = Event(type=io_done_type, job_id=job.id)
                time = last_event_time + time_remaining
                self.events.push(event, time)
                job.blocked = True
                return

        raise ValueError(f"Unrecognized task type: {task_type}")

    def tokenize_state(self):
        """
        Returns a tokenized encoding of the simulation state.
        """
        pass
        # TODO:
        # for each process
        # come up with a unique process ID vector
        # tokenize the process
        # concat the process ID vector to each of the tokens
        # add the tokens to the list of tokens
        # Sort the tokens so that the process tokens come first
        # return the tokens

    def is_finished(self):
        return not (self.events or self.jobs)
