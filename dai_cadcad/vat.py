""" Vat Module
    Class-based representation of the Vat smart contract
    (contains only what is necessary for the simulation)
"""

from dai_cadcad.pymaker.numeric import Wad, Rad, Ray
from dai_cadcad.util import require


class Ilk:
    id = ""
    Art = Wad(0)
    rate = Ray(0)
    spot = Ray(0)
    line = Rad(0)
    dust = Rad(0)

    def __init__(self, ilk_id):
        self.id = ilk_id


class Urn:
    ADDRESS = ""

    ink = Wad(0)
    art = Wad(0)

    def __init__(self, address, ink, art):
        self.ADDRESS = address

        self.ink = ink
        self.art = art


class Vat:
    ADDRESS = "vat"

    ilks = {}
    urns = {}
    gem = {}
    dai = {}
    sin = {}

    debt = Rad(0)
    vice = Rad(0)
    Line = Rad(0)

    def init(self, ilk_id):
        """ This specifically is *not* the __init__ method. """
        require(not self.ilks.get(ilk_id), "Vat/ilk-already-init")
        self.ilks[ilk_id] = Ilk(ilk_id)
        self.ilks[ilk_id].rate = Ray.from_number(1)

    def file(self, what, data):
        if what == "Line":
            self.Line = data
        else:
            raise Exception("Vat/file-unrecognized-param")

    def file_ilk(self, ilk_id, what, data):
        if what == "spot":
            self.ilks[ilk_id].spot = data
        elif what == "line":
            self.ilks[ilk_id].line = data
        elif what == "dust":
            self.ilks[ilk_id].dust = data
        else:
            raise Exception("Vat/file-unrecognized-param")

    def slip(self, ilk_id, usr, wad):
        usr_gem = self.gem[ilk_id].get(usr, Wad(0))
        usr_gem += wad
        self.gem[ilk_id][usr] = usr_gem

    def flux(self, ilk_id, src, dst, wad):
        self.gem[ilk_id][src] -= wad
        dst_gem = self.gem[ilk_id].get(dst, Wad(0))
        dst_gem += wad
        self.gem[ilk_id][dst] = dst_gem

    def move(self, src, dst, rad):
        self.dai[src] -= rad
        dst_dai = self.dai.get(dst, Rad(0))
        dst_dai += rad
        self.dai[dst] = dst_dai

    def frob(self, i, u, v, w, dink, dart):
        urn = self.urns[i].get(u, Urn(u, Wad(0), Wad(0)))
        ilk = self.ilks[i]

        urn.ink += dink
        urn.art += dart
        ilk.Art += dart

        dtab = Rad(ilk.rate * dart)
        tab = Rad(ilk.rate * urn.art)
        self.debt += dtab

        require(
            dart <= Wad(0)
            or (Rad(ilk.Art * ilk.rate) <= ilk.line and self.debt <= self.Line),
            "Vat/ceiling-exceeded",
        )
        require(
            dart <= Wad(0) <= dink or tab <= Rad(urn.ink * ilk.spot), "Vat/not-safe"
        )
        require(urn.art == Wad(0) or tab >= ilk.dust, "Vat/dust")

        self.gem[i][v] -= dink
        w_dai = self.dai.get(w, Rad(0))
        w_dai += dtab
        self.dai[w] = w_dai

        self.urns[i][u] = urn
        self.ilks[i] = i

    def grab(self, i, u, v, w, dink, dart):
        urn = self.urns[i][u]
        ilk = self.ilks[i]

        urn.ink += dink
        urn.art += dart
        ilk.Art += dart

        dtab = Rad(ilk.rate * dart)

        self.gem[i][v] -= dink
        self.sin[w] -= dtab
        self.vice -= dtab
