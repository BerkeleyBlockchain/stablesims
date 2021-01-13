""" Vow Module
    Class-based representation of the Vow smart contract
    (contains only what is necessary for the simulation)
"""

from pydss.pymaker.numeric import Rad, Wad


class Vow:
    """
    ADDRESS = str

    vat = Vat
    flapper = Flapper
    flopper = Flopper

    sin = dict[int: Rad]
    Sin = Rad
    Ash = Rad

    wait = int
    dump = Wad
    sump = Rad

    bump = Rad
    hump = Rad
    """

    def __init__(self, vat, flapper, flopper):
        self.ADDRESS = "vow"

        self.vat = vat
        self.flapper = flapper
        self.flopper = flopper

        self.sin = {}
        self.Sin = Rad(0)
        self.Ash = Rad(0)

        self.wait = 0
        self.dump = Wad(0)
        self.sump = Rad(0)

        self.bump = Rad(0)
        self.hump = Rad(0)

    def file(self, what, data):
        if what == "wait":
            self.wait = data
        elif what == "bump":
            self.bump = data
        elif what == "sump":
            self.sump = data
        elif what == "dump":
            self.dump = data
        elif what == "hump":
            self.hump = data
        elif what == "flapper":
            self.flapper = data
        elif what == "flopper":
            self.flopper = data
        else:
            raise Exception("Vow/file-unrecognized-param")

    def fess(self, tab, now):
        # TODO: Remove `now` parameter if/when another solution for providing time / other
        # contextual info is implemented
        if not self.sin.get(now):
            self.sin[now] = Rad(0)
        self.sin[now] += tab
        self.Sin += tab
