""" Join Module
    Class-based representation of the various Join smart contracts
    (contains only what is necessary for the simulation)
"""

from dai_cadcad.pymaker.numeric import Wad, Rad
from dai_cadcad.util import require


class GemJoin:
    ADDRESS = ""

    vat = None
    ilk = ""
    gem = None

    def __init__(self, vat, ilk, gem):
        self.vat = vat
        self.ilk = ilk
        self.gem = gem

    def join(self, sender, usr, wad):
        require(wad >= Wad(0), "GemJoin/overflow")
        self.vat.slip(self.ilk, usr, wad)
        require(
            self.gem.transferFrom(sender, self.ADDRESS, float(wad)),
            "GemJoin/failed-transfer",
        )

    def exit(self, sender, usr, wad):
        require(wad <= Wad(2 ** 255), "GemJoin/overflow")
        self.vat.slip(self.ilk, sender, Wad(0) - wad)
        require(
            self.gem.transferFrom(self.ADDRESS, usr, float(wad)),
            "GemJoin/failed-transfer",
        )


class DaiJoin:
    ADDRESS = "dai_join"

    vat = None
    dai = None

    def __init__(self, vat, dai):
        self.vat = vat
        self.dai = dai

    def join(self, sender, usr, wad):
        self.vat.move(self.ADDRESS, usr, Rad(wad))
        self.dai.burn(sender, float(wad))

    def exit(self, sender, usr, wad):
        self.vat.move(sender, self.ADDRESS, Rad(wad))
        self.dai.mint(usr, float(wad))
