# TODO: scheduler metrics
# takes in a history and a job priority and spits out a metric
from event_queue import find_event
from simulation import SWITCHING_DONE


def weighted_mean_turnaround_time(history, job_priorities):
    # add 1 to the priority
    # divide the turnaround time by (1+priority)
    total_turnaround_time = 0
    total_weight = 0
    for job_id, priority in job_priorities.items():
        job_start_time, _ = history[find_event(history, job_id=job_id)]
        job_end_time, _ = history[find_event(history, job_id=job_id, get_last=True)]
        weight = 1 / (1 + priority)
        total_turnaround_time = (job_end_time - job_start_time) * weight
        total_weight += weight
    return total_turnaround_time / total_weight


def weighted_mean_response_time(history, job_priorities):
    total_response_time = 0
    total_weight = 0
    for job_id, priority in job_priorities.items():
        job_start_time, _ = history[find_event(history, job_id=job_id)]
        job_run_time, _ = history[
            find_event(history, job_id=job_id, event_type=SWITCHING_DONE)
        ]
        total_response_time = (job_run_time - job_start_time) / (1 + priority)
        total_weight += 1 / (1 + priority)
    return total_response_time / total_weight
