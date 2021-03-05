""" Abaci Module
    Class-based representation of the Abaci smart contract
    (contains only what is necessary for the simulation)
"""

from pydss.pymaker.numeric import Wad, Rad
from pydss.util import require


class Abaci:
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
        return top * (tau - dur) / tau  # TODO: need to cast to Rad
