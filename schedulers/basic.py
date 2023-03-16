import random


class RandomScheduler:
    def __init__(self):
        pass

    def schedule(self, simulation):
        return random.choice(list(simulation.jobs.keys()))


class RoundRobinScheduler:
    def __init__(self):
        self.queue = []

    def schedule(self, simulation):
        # Add new jobs to the front of the queue
        new_job_ids = [
            job_id for job_id in simulation.jobs.keys() if job_id not in self.queue
        ]
        self.queue = new_job_ids + self.queue
        while self.queue[0] not in simulation.jobs:
            self.queue.pop(0)
        assert self.queue, "No more jobs to schedule!"
        # run the first job, then move it to the back
        job_to_run = self.queue.pop(0)
        self.queue.append(job_to_run)
        return job_to_run


class FIFOScheduler:
    def __init__(self):
        self.queue = []

    def schedule(self, simulation):
        # Add new jobs to the back of the queue
        new_job_ids = [
            job_id for job_id in simulation.jobs.keys() if job_id not in self.queue
        ]
        self.queue += new_job_ids
        while self.queue[0] not in simulation.jobs:
            self.queue.pop(0)
        assert self.queue, "No more jobs to schedule!"
        # just keep running the first job till its done
        return self.queue[0]
