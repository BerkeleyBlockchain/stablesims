""" Dog Module
    Class-based representation of the Dog smart contract
    (contains only what is necessary for the simulation)
"""

from pydss.pymaker.numeric import Wad, Rad, Ray
from pydss.util import require


class Ilk:
    """
    id = str
    clip = Clipper
    chop = Wad
    hole = Rad
    dirt = Rad
    """

    def __init__(self, ilk_id):
        self.id = ilk_id
        self.chop = Wad(0)
        self.hole = Rad(0)
        self.dirt = Rad(0)


class Dog:
    """
    vat = Vat
    ilks = dict[str: Ilk]
    vow = Vow
    Hole = Rad
    Dirt = Rad
    """

    def __init__(self, vat):
        self.vat = vat
        self.vow = None
        self.Hole = Rad(0)
        self.Dirt = Rad(0)
        self.ilks = {}

    def file(self, what, data):
        if what == "vow":
            self.vow = data
        elif what == "Hole":
            self.Hole = data
        else:
            raise Exception("Dog/file-unrecognized-param")

    def file_ilk(self, ilk_id, what, data):
        if what in ("chop", "hole", "clip"):
            if not self.ilks.get(ilk_id):
                self.ilks[ilk_id] = Ilk(ilk_id)
            if what == "chop":
                self.ilks[ilk_id].chop = data
            elif what == "hole":
                self.ilks[ilk_id].hole = data
            elif what == "clip":
                self.ilks[ilk_id].clip = data
        else:
            raise Exception("Dog/file-unrecognized-param")

    def bark(self, ilk_id, urn_id, kpr, now):
        ink = self.vat.urns[ilk_id][urn_id].ink
        art = self.vat.urns[ilk_id][urn_id].art
        milk = self.ilks[ilk_id]

        rate = self.vat.ilks[ilk_id].rate
        spot = self.vat.ilks[ilk_id].spot
        dust = self.vat.ilks[ilk_id].dust
        require(spot > Ray(0) and spot * ink < rate * art, "Dog/not-unsafe")

        room = min(self.Hole - self.Dirt, milk.hole - milk.dirt)
        require(room > Rad(0) and room >= dust, "Dog/liquidation-limit-hit")

        dart = min(art, Wad(room / Rad(rate)) / milk.chop)

        if Rad(rate * (art - dart)) < dust:
            # Q: What if art > room?
            # Resetting dart = art here can push past liq limit
            dart = art

        dink = ink * dart / art

        require(dink > Wad(0), "Dog/null-auction")
        require(
            dart <= Wad.from_number(2 ** 255) and dink <= Wad.from_number(2 ** 255),
            "Dog/overflow",
        )

        self.vat.grab(
            ilk_id,
            urn_id,
            milk.clip.ADDRESS,
            self.vow.ADDRESS,
            Wad(0) - dink,
            Wad(0) - dart,
        )

        due = Rad(rate * dart)
        self.vow.fess(due, now)

        tab = due * Rad(milk.chop)
        self.Dirt += tab
        self.ilks[ilk_id].dirt = milk.dirt + tab

        milk.clip.kick(tab, dink, urn_id, kpr, now)
        return [tab]

    def digs(self, ilk_id, rad):
        self.Dirt -= rad
        self.ilks[ilk_id].dirt -= rad
