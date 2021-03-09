""" Join Module
    Class-based representation of the various Join smart contracts
    (contains only what is necessary for the simulation)
"""

from pydss.pymaker.numeric import Wad, Rad
from pydss.util import require


class GemJoin:
    """
    ADDRESS = ""

    vat = Vat
    ilk_id = ""
    gem = Token
    """

    def __init__(self, vat, ilk_id, gem):
        self.ADDRESS = f"gem_join-{ilk_id}"
        self.vat = vat
        self.ilk_id = ilk_id
        self.gem = gem

    def join(self, sender, usr, wad):
        require(wad >= Wad(0), "GemJoin/overflow")
        self.vat.slip(self.ilk_id, usr, wad)
        require(
            self.gem.transferFrom(sender, self.ADDRESS, float(wad)),
            "GemJoin/failed-transfer",
        )

    def exit(self, sender, usr, wad):
        require(wad <= Wad(2 ** 255), "GemJoin/overflow")
        self.vat.slip(self.ilk_id, sender, Wad(0) - wad)
        require(
            self.gem.transferFrom(self.ADDRESS, usr, float(wad)),
            "GemJoin/failed-transfer",
        )


class DaiJoin:
    """
    ADDRESS = str

    vat = Vat
    dai = Token
    """

    def __init__(self, vat, dai):
        self.ADDRESS = "dai_join"
        self.vat = vat
        self.dai = dai

    def join(self, sender, usr, wad):
        self.vat.move(self.ADDRESS, usr, Rad(wad))
        self.dai.burn(sender, float(wad))

    def exit(self, sender, usr, wad):
        self.vat.move(sender, self.ADDRESS, Rad(wad))
        self.dai.mint(usr, float(wad))
