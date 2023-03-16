from job import Job, Task, COMPUTE, MEMORY, DISK, NETWORK
import random
import numpy as np

END = "end"


def task_distribution_factory():
    log_time_means = {
        COMPUTE: 0,
        MEMORY: 1,
        DISK: 1.5,
        NETWORK: 1.5,
    }  # TODO randomly generate
    log_time_stds = {
        COMPUTE: 1,
        MEMORY: 1,
        DISK: 0.2,
        NETWORK: 0.5,
    }  # TODO randomly generate
    task_types = [COMPUTE, MEMORY, DISK, NETWORK, END]

    task_weights = np.random.randint(1, 10, size=len(task_types))
    task_weights = task_weights / task_weights.sum()
    task_cdf = list(np.cumsum(task_weights))

    def task_distribution():
        # Choose a task type from the distribution
        x = random.random()
        i = 0
        while x > task_cdf[i] and i < len(task_cdf):
            i += 1
        task_type = task_types[i]
        if task_type == END:
            return END

        # Randomly sample the time remaining
        log_time_mean = log_time_means[task_type]
        log_time_std = log_time_stds[task_type]
        log_time_remaining = random.gauss(log_time_mean, log_time_std)
        time_remaining = max(1, int(10 ** (log_time_remaining)))

        return Task(task_type, time_remaining)

    return task_distribution


def make_job_timeline(n_jobs, max_start_time, get_task_distribution):
    job_timeline = []
    while len(job_timeline) < n_jobs:
        task_distribution = get_task_distribution()
        tasks = []
        while True:
            task = task_distribution()
            if task == END:
                break
            tasks.append(task)
        if len(tasks) == 0:
            continue
        if len(job_timeline) == 0:
            start_time = 0
        else:
            start_time = random.randint(0, max_start_time)
        priority = random.randint(0, 4)
        job = Job(None, priority, tasks)
        job_timeline.append((start_time, job))

    return sorted(job_timeline, key=lambda k: k[0])
