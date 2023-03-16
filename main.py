# Run a simulation and print out the result
import argparse
from schedulers.priority import WeightedRandomScheduler
from schedulers.basic import RandomScheduler, RoundRobinScheduler, FIFOScheduler
from job_timeline import make_job_timeline, task_distribution_factory
from simulation import Simulation
from metrics import weighted_mean_turnaround_time, weighted_mean_response_time
import numpy as np
import matplotlib.pyplot as plt
import torch


def execute_simulations(scheduler_type, num_jobs, max_start_time, num_runs):
    turnaround = []
    response = []

    for run in range(num_runs):
        # create the job timeline
        job_timeline = make_job_timeline(
            num_jobs, max_start_time, task_distribution_factory
        )
        # create the simulation
        simulation = Simulation(job_timeline)
        # create the scheduler
        if scheduler_type == "RR":
            scheduler = RoundRobinScheduler()
        elif scheduler_type == "random":
            scheduler = RandomScheduler()
        elif scheduler_type == "FIFO":
            scheduler = FIFOScheduler()
        elif scheduler_type == "weightedRandom":
            scheduler = WeightedRandomScheduler()
        else:
            raise ValueError(f"Unrecognized scheduler type: {scheduler_type}")

        # Run the simulation
        simulation.run_until_scheduling_needed()
        while not simulation.is_finished():
            try:
                simulation.schedule_job(scheduler.schedule(simulation))
            except IndexError as ie:
                import pdb

                pdb.set_trace()
            simulation.run_until_scheduling_needed()

        # Evaluate metrics
        job_priorities = {
            job.id: job.priority for start_time, job in job_timeline
        }  # TODO
        mean_trt = weighted_mean_turnaround_time(simulation.history, job_priorities)
        mean_rt = weighted_mean_response_time(simulation.history, job_priorities)

        turnaround.append(mean_trt)
        response.append(mean_rt)

    turnaround = np.array(turnaround)
    response = np.array(response)
    return turnaround, response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run simulations of a process scheduler with the given parameters"
    )
    parser.add_argument(
        "--scheduler_type",
        type=str,
        default="random",
        help="One of {'RR', 'random', 'FIFO', 'weightedRandom'}",
    )
    parser.add_argument(
        "--num_jobs",
        type=int,
        default=100,
        help="How many jobs to create in a given simulation?",
    )
    parser.add_argument(
        "--max_start_time",
        default=1000,
        help="What's the latest start time a job can have? Job start times are uniformly sampled between 0 and this value.",
    )
    parser.add_argument(
        "--num_runs", type=int, default=1, help="How many times to run the simulation"
    )
    args = parser.parse_args()

    turnaround, response = execute_simulations(
        args.scheduler_type, args.num_jobs, args.max_start_time, args.num_runs
    )
    print(f"Mean turnaround time: {turnaround.mean():.01f} +- {turnaround.std():.01f}")
    print(f"Mean response time: {response.mean():.01f} +- {response.std():.01f}")

# TODO: plot histograms of turnaround time and response time
