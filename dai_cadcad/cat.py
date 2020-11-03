""" Cat Module
    Class-based representation of the Cat smart contract
    (contains only what is necessary for the simulation)
"""

from operator import itemgetter

from dai_cadcad.pymaker.numeric import Wad, Rad, Ray
from dai_cadcad.util import require


class Ilk:
    ilk_id = ""
    flip = None
    chop = Wad(0)
    dunk = Rad(0)

    def __init__(self, ilk_id, flip, chop, dunk):
        self.ilk_id = ilk_id
        self.flip = flip
        self.chop = chop
        self.dunk = dunk


class Cat:
    ADDRESS = "cat"

    ilks = {}

    vat = None
    vow = None
    box = Rad(0)
    litter = Rad(0)

    def __init__(self, ilks, vat, vow, box):
        """ `ilks` must be an array containing a configuration object for each ilk type of the
            following form:
            {
                "ilk_id": str,
                "flip": Flipper,
                "chop": Wad,
                "dunk": Rad
            }
        """

        self.vat = vat
        self.vow = vow
        self.box = box

        for ilk in ilks:
            self.ilks[ilk["ilk_id"]] = Ilk(
                ilk["ilk_id"], ilk["flip"], ilk["chop"], ilk["dunk"]
            )

    def bite(self, ilk, urn, now):
        # TODO: Remove `now` once better timekeeping solution is implemented

        rate, spot, dust = itemgetter("rate", "spot", "dust")(self.vat.ilks[ilk])
        ink, art = itemgetter("ink", "art")(self.vat.urns[ilk][urn])

        require(spot > Ray(0) and Rad(ink * spot) < Rad(art * rate), "Cat/not-unsafe")

        milk = self.ilks[ilk]

        room = self.box - self.litter
        require(self.litter < self.box and room >= dust, "Cat/liquidation-limit-hit")

        dart = Wad.min(art, Wad(Rad.min(milk.dunk, room)) / Wad(rate) / milk.chop)
        dink = Wad.min(ink, ink * dart / art)

        require(dart > Wad(0) and dink > Wad(0), "Cat/null-auction")
        require(
            dart <= Wad.from_number(2 ** 255) and dink <= Wad.from_number(2 ** 255),
            "Cat/overflow",
        )

        self.vat.grab(
            ilk, urn, self.ADDRESS, self.vow.ADDRESS, Wad(0) - dink, Wad(0) - dart
        )
        self.vow.fess(Rad(dart * rate))

        tab = Rad(dart * rate * milk.chop)
        self.litter += tab

        milk.flip.kick(urn, self.vow.ADDRESS, tab, dink, Rad(0), now)

    def claw(self, rad):
        self.litter -= rad
