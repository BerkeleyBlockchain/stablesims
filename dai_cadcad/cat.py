""" Cat Module
    Class-based representation of the Cat smart contract
    (contains only what is necessary for the simulation)
"""

from operator import itemgetter

from dai_cadcad.pymaker.numeric import Wad, Rad, Ray
from dai_cadcad.util import require


class Ilk:
    id = ""
    flip = None
    chop = Wad(0)
    dunk = Rad(0)

    def __init__(self, ilk_id):
        self.id = ilk_id


class Cat:
    ADDRESS = "cat"

    ilks = {}

    vat = None
    vow = None
    box = Rad(0)
    litter = Rad(0)

    def __init__(self, vat):
        self.vat = vat

    def file(self, what, data):
        # TODO: Typechecking here?
        if what == "vow":
            self.vow = data
        elif what == "box":
            self.box = data
        else:
            # TODO: Custom exception classes?
            raise Exception("Cat/file-unrecognized-param")

    def file_ilk(self, ilk_id, what, data):
        if what in ("chop", "dunk", "flip"):
            if not self.ilks.get(ilk_id):
                self.ilks[ilk_id] = Ilk(ilk_id)
            if what == "chop":
                self.ilks[ilk_id].chop = data
            elif what == "dunk":
                self.ilks[ilk_id].dunk = data
            elif what == "flip":
                # TODO: nope-ing & hope-ing here
                self.ilks[ilk_id].flip = data

    def bite(self, ilk_id, urn, now):
        # TODO: Remove `now` once better timekeeping solution is implemented

        rate, spot, dust = itemgetter("rate", "spot", "dust")(self.vat.ilks[ilk_id])
        ink, art = itemgetter("ink", "art")(self.vat.urns[ilk_id][urn])

        require(spot > Ray(0) and Rad(ink * spot) < Rad(art * rate), "Cat/not-unsafe")

        milk = self.ilks[ilk_id]

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
            ilk_id, urn, self.ADDRESS, self.vow.ADDRESS, Wad(0) - dink, Wad(0) - dart
        )
        self.vow.fess(Rad(dart * rate))

        tab = Rad(dart * rate * milk.chop)
        self.litter += tab

        milk.flip.kick(urn, self.vow.ADDRESS, tab, dink, Rad(0), now)

    def claw(self, rad):
        self.litter -= rad
