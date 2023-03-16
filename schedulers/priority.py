import random

# TODO: like the basic schedulers, but with additional
# tooling for priorities.


class WeightedRandomScheduler:
    """Randomly selects a job to run, weighted towards the higher-priority jobs."""

    def __init__(self):
        pass

    def schedule(self, simulation):
        job_weights = {
            job.id: 1 / (1 + job.priority) for job in simulation.jobs.values()
        }
        # TODO: why isn't this working as expected?
        total_weight = sum(job_weights.values())
        job_weights = [
            (job_id, (weight / total_weight) ** (1 / 2))
            for job_id, weight in job_weights.items()
        ]
        job_id = random.choices(
            [key for key, _ in job_weights],
            [weight for _, weight in job_weights],
        )[0]

        return job_id
