import random
import time


class Mock:
    def __init__(self, dim=3):
        self.dim = dim
        random.seed(time.time())

    def initialize(self):  # pylint: disable=no-self-use
        pass

    def finalize(self):  # pylint: disable=no-self-use
        pass

    def get_states(self):  # pylint: disable=no-self-use
        return time.time(), [random.randint(-100, 100) for i in range(self.dim)]
