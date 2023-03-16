from collections import namedtuple

COMPUTE = "COMPUTE"
MEMORY = "MEMORY"
DISK = "DISK"
NETWORK = "NETWORK"

Task = namedtuple("Task", ["type", "time_remaining"])


class Job:
    def __init__(self, job_id, priority, instructions):
        pass
        self.id = job_id
        self.priority = priority
        self.instructions = instructions
        self.blocked = False
        self.remaining_tasks = instructions.copy()  # starts as a copy of instructions

    def __str__(self):
        return f"id={self.id}, priority={self.priority}, blocked={self.blocked}, remaining_tasks={self.remaining_tasks}"

    def __repr__(self):
        return f"id={self.id}, priority={self.priority}, blocked={self.blocked}, remaining_tasks={self.remaining_tasks}"
