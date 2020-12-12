""" Spotter Module
    Class-based representation of the Spotter smart contract
    (contains only what is necessary for the simulation)
"""

import json

from dai_cadcad.pymaker.numeric import Wad, Ray


class Ilk:
    id = ""
    pip = None
    mat = Ray(0)

    def __init__(self, ilk_id):
        self.id = ilk_id


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

    def __init__(self, vat):
        self.vat = vat

    def file(self, what, data):
        if what == "par":
            self.par = data
        else:
            raise Exception("Spotter/file-unrecognized-param")

    def file_ilk(self, ilk_id, what, data):
        if what in ("pip", "mat"):
            if not self.ilks.get(ilk_id):
                self.ilks[ilk_id] = Ilk(ilk_id)
            if what == "pip":
                self.ilks[ilk_id].pip = data
            elif what == "mat":
                self.ilks[ilk_id].mat = data
            else:
                raise Exception("Spotter/file-unrecognized-param")

    def poke(self, ilk_id, now):
        val = self.ilks[ilk_id]["pip"].peek(now)
        spot = Ray(val) / self.par / self.ilks[ilk_id].mat
        self.vat.file(ilk_id, "spot", spot)
