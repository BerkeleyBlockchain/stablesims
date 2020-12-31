""" Vow Module
    Class-based representation of the Vow smart contract
    (contains only what is necessary for the simulation)
"""

from pydss.pymaker.numeric import Rad, Wad


class Vow:
    ADDRESS = "vow"

    vat = None
    flapper = None
    flopper = None

    sin = {}
    Sin = Rad(0)
    Ash = Rad(0)

    wait = 0
    dump = Wad(0)
    sump = Rad(0)

    bump = Rad(0)
    hump = Rad(0)

    def __init__(self, vat, flapper, flopper):
        self.vat = vat
        self.flapper = flapper
        self.flopper = flopper

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
        self.sin[now] += tab
        self.Sin += tab
