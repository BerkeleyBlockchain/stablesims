""" Vat Module
    Class-based representation of the Vat smart contract
    (contains only what is necessary for the simulation)
"""

from dai_cadcad.pymaker.numeric import Wad, Rad, Ray
from dai_cadcad.util import require


class Ilk:
    ilk_id = ""
    Art = Wad(0)
    rate = Ray(0)
    spot = Ray(0)
    line = Rad(0)
    dust = Rad(0)

    def __init__(self, ilk_id, Art, rate, spot, line, dust):
        self.ilk_id = ilk_id
        self.Art = Art
        self.rate = rate
        self.spot = spot
        self.line = line
        self.dust = dust


class Urn:
    ink = Wad(0)
    art = Wad(0)

    def __init__(self, ink, art):
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

    def __init__(self, line, ilks):
        """ `ilks` must be an array containing a configuration abject for each ilk type of the
            following form:
                {
                    "ilk_id": str,
                    "rate": Ray,
                    "line": Rad,
                    "dust": Rad
                }
        """

        self.Line = line

        for ilk in ilks:
            ilk_id = ilk["ilk_id"]
            self.ilks[ilk_id] = Ilk(
                ilk_id, Wad(0), ilk["rate"], Ray(0), ilk["line"], ilk["dust"]
            )
            self.urns[ilk_id] = {}
            self.gem[ilk_id] = {}

    def file(self, what, data):
        if what == "Line":
            self.Line = data

    def file_ilk(self, ilk, what, data):
        if what == "spot":
            self.ilks[ilk].spot = data
        elif what == "line":
            self.ilks[ilk].line = data
        elif what == "dust":
            self.ilks[ilk].dust = data

    def slip(self, ilk, usr, wad):
        usr_gem = self.gem[ilk].get(usr, Wad(0))
        usr_gem += wad
        self.gem[ilk][usr] = usr_gem

    def flux(self, ilk, src, dst, wad):
        self.gem[ilk][src] -= wad
        self.gem[ilk][dst] += wad

    def move(self, src, dst, rad):
        self.dai[src] -= rad
        self.dai[dst] += rad

    def frob(self, i, u, v, w, dink, dart):
        urn = self.urns[i].get(u, Urn(Wad(0), Wad(0)))
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
