""" Abaci Module
    Class-based representation of the Abaci smart contract
    (contains only what is necessary for the simulation)
"""

from pydss.pymaker.numeric import Wad, Rad
from pydss.util import require


class Abaci:
    """
    """

    def __init__(self):
        pass

    def file(self, what, data):
        pass

    def price(self, top, dur):
        """
        top: initial price
        dur: seconds since action has started
        """
        pass


class LinearDecrease(Abaci):
    """
    tau = int
    """

    def __init__(self):
        self.tau = 0
        super().__init__()

    def file(self, what, data):
        if what == "tau":
            self.tau = data
        else:
            raise Exception("LinearDecrease/file-unrecognized-param")

    def price(self, top, dur):
        if dur >= self.tau:
            return 0
        return top * (self.tau - dur) / self.tau  # TODO: need to cast to Rad


class StairstepExponentialDecrease(Abaci):
    """
    step = int, seconds between price drop
    cut = int, percentage to decrease
    """

    def __init__(self):
        self.step = 0
        self.cut = 0
        super().__init__()

    def file(self, what, data):
        if what == "cut":
            self.cut = data  # TODO: Maker uses require here?
        elif what == "step":
            self.step = data
        else:
            raise Exception("StairstepExponentialDecrease/file-unrecognized-param")

    def price(self, top, dur):
        return top * (self.cut ** (dur / self.step))
