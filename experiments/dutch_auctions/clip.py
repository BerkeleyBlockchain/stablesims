""" Clipper Module
    Class-based representation of the Clipper smart contract
    (contains only what is necessary for the simulation)
"""

from pydss.pymaker.numeric import Wad, Rad, Ray
from pydss.util import require


class Sale:
    """
    id = str
    pos = int
    tab = Rad
    lot = Wad
    usr = str
    tic = int
    top = Ray
    """

    def __init__(self, pos, tab, lot, usr, tic, top, sale_id):
        self.pos = pos
        self.tab = tab
        self.lot = lot
        self.usr = usr
        self.tic = tic
        self.top = top
        self.id = sale_id


class Clipper:
    """
    ADDRESS = str

    ilk_id = str
    vat = Vat
    dog = Dog

    vow = Vow  // in source this is the vow's address, not an interface
    spotter = Spotter
    calc = Abacus

    buf = Ray
    tail = int
    cusp = Ray

    kicks = int
    active = list[str]

    sales = dict[int: Sale]

    locked = int
    stopped = int

    chip = Wad
    tip = Rad
    """

    def __init__(self, vat, spotter, dog, ilk_id):
        self.vat = vat
        self.spotter = spotter
        self.dog = dog
        self.ilk_id = ilk_id
        self.buf = Ray.from_number(1)

        self.vow = None
        self.calc = None
        self.tail = 0
        self.cusp = Ray(0)
        self.kicks = 0
        self.active = []
        self.sales = {}
        self.locked = 0
        self.stopped = 0
        self.chip = Wad(0)
        self.tip = Rad(0)

    def file(self, what, data):
        if what == "buf":
            self.buf = data
        elif what == "tail":
            self.tail = data
        elif what == "cusp":
            self.cusp = data
        elif what == "chip":
            self.chip = data
        elif what == "tip":
            self.tip = data
        else:
            raise Exception("Clipper/file-unrecognized-param")

    def file_address(self, what, data):
        if what == "spotter":
            self.spotter = data
        elif what == "vow":
            self.vow = data
        elif what == "calc":
            self.calc = data
        else:
            raise Exception("Clipper/file-unrecognized-param")

    def kick(self, tab, lot, usr, kpr, now):
        require(tab > Rad(0), "Clipper/zero-tab")
        require(lot > Wad(0), "Clipper/zero-lot")
        require(bool(usr), "Clipper/zero-usr")
        require(self.kicks < (1 << 31) - 1, "Clipper/overflow")

        self.kicks += 1
        sale_id = self.kicks

        pip = self.spotter.ilks[self.ilk_id]
        val = pip.peek(now)

        self.sales[sale_id] = Sale(
            len(self.active) - 1,
            tab,
            lot,
            usr,
            now,
            Ray(val / Wad(self.spotter.par)) * self.buf,
            sale_id,
        )

        if self.tip > 0 or self.chip > 0:
            self.vat.suck(self.vow.ADDRESS, kpr, self.tip + tab * Rad(self.chip))
