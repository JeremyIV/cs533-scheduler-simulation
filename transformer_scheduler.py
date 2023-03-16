class SchedulerModule(nn.Module):
    def __init__(self):
        super().__init__()
        pass

    def forward(self, simulation_state):
        """Takes in a simulation state
        as an array of tokens.
        The first tokens should be the job tokens.
        Performs several layers of self-attention,
        then queries only for the job tokens.
        Then feeds the results through an MLP
        and chooses the job with the highest activation.
        """


class transformer_scheduler:
    def __init__(self):
        pass

    def schedule(self, simulation):
        pass
        # TODO:
        # tokenize the simulation
        # pass it into the network
        # get the job token with the greatest activation
        # (or should I do softmax prob. sampling?)
        # return the id of that job
