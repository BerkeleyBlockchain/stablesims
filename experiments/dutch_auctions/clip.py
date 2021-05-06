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


def is_stopped(level):
    def is_stopped_decorator(func):
        def wrapped_func(self, *args, **kwargs):
            require(self.stopped < level, "Clipper/stopped-incorrect")
            func(self, *args, **kwargs)

        return wrapped_func

    return is_stopped_decorator


def lock(func):
    def wrapped_func(self, *args, **kwargs):
        require(self.locked == 0, "Clipper/system-locked")
        self.locked = 1
        func(self, *args, **kwargs)
        self.locked = 0

    return wrapped_func


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
        self.ADDRESS = f"clipper-{ilk_id}"

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

    @is_stopped(1)
    def kick(self, tab, lot, usr, kpr, now):
        require(tab > Rad(0), "Clipper/zero-tab")
        require(lot > Wad(0), "Clipper/zero-lot")
        require(bool(usr), "Clipper/zero-usr")
        require(self.kicks < (1 << 31) - 1, "Clipper/overflow")

        self.kicks += 1
        sale_id = self.kicks
        self.active.append(sale_id)

        pip = self.spotter.ilks[self.ilk_id].pip
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

        if self.tip > Rad(0) or self.chip > Wad(0):
            self.vat.suck(self.vow.ADDRESS, kpr, self.tip + tab * Rad(self.chip))

    def status(self, tic, top, now):
        price = self.calc.price(top, now - tic)
        done = now - tic > self.tail or Ray(price) / top < self.cusp
        return (done, price)

    @lock
    @is_stopped(2)
    def redo(self, sale_id, kpr, now):
        usr = self.sales[sale_id].usr
        tic = self.sales[sale_id].tic
        top = self.sales[sale_id].top

        require(bool(usr), "Clipper/not-running-auction")

        (done, _) = self.status(tic, top, now)
        require(done, "Clipper/cannot-reset")

        tab = self.sales[sale_id].tab
        lot = self.sales[sale_id].lot
        self.sales[sale_id].tic = now

        pip = self.spotter.ilks[self.ilk_id].pip
        val = pip.peek(now)
        price = Ray(val / Wad(self.spotter.par))
        self.sales[sale_id].top = price * self.buf

        if self.tip > Rad(0) or self.chip > Wad(0):
            dust = self.vat.ilks[self.ilk_id].dust
            if tab >= dust and Rad(lot * price) >= dust:
                self.vat.suck(self.vow.ADDRESS, kpr, self.tip + tab * Rad(self.chip))

    @lock
    @is_stopped(2)
    def take(self, sale_id, amt, max_price, who, data, now, sender):
        require(self.sales.get(sale_id), "Clipper/not-running-auction")
        usr = self.sales[sale_id].usr
        tic = self.sales[sale_id].tic

        (done, price) = self.status(tic, self.sales[sale_id].top, now)
        require(not done, "Clipper/needs-reset")

        require(max_price >= price, "Clipper/too-expensive")

        lot = self.sales[sale_id].lot
        tab = self.sales[sale_id].tab

        lot_slice = min(lot, amt)
        owe = Rad(price * lot_slice)

        if owe > tab:
            owe = tab
            lot_slice = Wad(owe / Rad(price))
        elif owe < tab and lot_slice < lot:
            dust = self.vat.ilks[self.ilk_id].dust
            if tab - owe < dust:
                require(tab > dust, "Clipper/no-partial-purchase")
                owe = tab - dust
                lot_slice = Wad(owe / Rad(price))

        tab = tab - owe
        lot = lot - lot_slice

        self.vat.flux(self.ilk_id, self.ADDRESS, who, lot_slice)

        if len(data) > 0 and who != self.vat.ADDRESS and who != self.dog.ADDRESS:
            who.clipperCall(sender, owe, lot_slice, data)

        self.vat.move(sender, self.vow.ADDRESS, owe)

        self.dog.digs(self.ilk_id, owe)

        if lot == Wad(0):
            self._remove(sale_id)
        elif tab == Rad(0):
            self.vat.flux(self.ilk_id, self.ADDRESS, usr, lot)
            self._remove(sale_id)
        else:
            self.sales[sale_id].tab = tab
            self.sales[sale_id].lot = lot

    def _remove(self, sale_id):
        _index = self.sales[sale_id].pos
        _move = self.active[-1]
        self.active[_index] = _move
        self.sales[_move].pos = _index
        self.active.pop()
        del self.sales[sale_id]
