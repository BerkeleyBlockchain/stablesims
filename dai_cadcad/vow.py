""" Vow Module
    Class-based representation of the Vow smart contract
    (contains only what is necessary for the simulation)
"""

from dai_cadcad.pymaker.numeric import Rad, Wad


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

    def __init__(self, wait, dump, sump, bump, hump):
        self.wait = wait
        self.dump = dump
        self.sump = sump
        self.bump = bump
        self.hump = hump

    def fess(self, tab, now):
        # TODO: Remove `now` parameter if/when another solution for providing time / other
        # contextual info is implemented
        self.sin[now] += tab
        self.Sin += tab
