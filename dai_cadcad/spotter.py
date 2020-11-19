""" Spotter Module
    Class-based representation of the Spotter smart contract
    (contains only what is necessary for the simulation)
"""

import json

from dai_cadcad.pymaker.numeric import Wad, Ray


class Ilk:
    id = ""
    pip = ""
    mat = Ray(0)

    def __init__(self, ilk_id, pip, mat):
        self.id = ilk_id
        self.pip = pip
        self.mat = mat


class PipLike:
    price_feed_file = ""

    def __init__(self, price_feed_file):
        self.price_feed_file = price_feed_file

    def peek(self, now):
        with open(self.price_feed_file) as price_feed_json:
            return Wad.from_number(
                # TODO: Constantize the "price_close" field here
                json.load(price_feed_json)[now]["price_close"]
            )


class Spotter:
    ADDRESS = ""

    ilks = {}

    vat = None
    par = Ray(0)

    def __init__(self, ilks, vat, par):
        """ `ilks` must be an array containing a configuration object for each ilk type of the
            following form:
            {
                "ilk_id": str,
                "pip": PipLike,
                "mat": Ray,
            }
        """

        self.vat = vat
        self.par = par

        for ilk in ilks:
            self.ilks[ilk["ilk_id"]] = Ilk(ilk["ilk_id"], ilk["pip"], ilk["mat"])

    def poke(self, ilk_id, now):
        val = self.ilks[ilk_id]["pip"].peek(now)
        spot = Ray(val) / self.par / self.ilks[ilk_id].mat
        self.vat.file(ilk_id, "spot", spot)
