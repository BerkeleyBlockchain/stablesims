""" Abaci Module
    Class-based representation of the Abaci smart contract
    (contains only what is necessary for the simulation)
"""

from pydss.pymaker.numeric import Ray
from pydss.util import require


class Abacus:
    """ Defines a price curve for a dutch auction.
    """

    def file(self, what, data):
        pass

    def price(self, top, dur):
        """
        top: initial price
        dur: seconds since action has started
        """


class LinearDecrease(Abacus):
    """
    tau = int
    """

    def __init__(self):
        self.tau = 0

    def file(self, what, data):
        if what == "tau":
            self.tau = data
        else:
            raise Exception("LinearDecrease/file-unrecognized-param")

    def price(self, top, dur):
        if dur >= self.tau:
            return 0
        return top * Ray.from_number((self.tau - dur) / self.tau)


class StairstepExponentialDecrease(Abacus):
    """
    step = int, seconds between price drop
    cut = Ray, percentage to decrease
    """

    def __init__(self):
        self.step = 0
        self.cut = Ray(0)

    def file(self, what, data):
        if what == "cut":
            require(data <= 10 ** 27, "StairstepExponentialDecrease/cut-gt-RAY")
            self.cut = data
        elif what == "step":
            self.step = data
        else:
            raise Exception("StairstepExponentialDecrease/file-unrecognized-param")

    def price(self, top, dur):
        return top * (self.cut ** Ray.from_number(dur / self.step))
