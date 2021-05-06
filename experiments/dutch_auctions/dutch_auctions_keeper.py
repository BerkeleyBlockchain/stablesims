""" Dutch Auctions Keeper Module
    Extension of the Keeper module which accomodates the new
    Dutch auction liquidation system.
"""

from pydss.keeper import VaultKeeper
from pydss.pymaker.numeric import Wad, Rad, Ray


class BarkKeeper(VaultKeeper):
    """
    dog = Dog
    vat = Vat
    """

    def __init__(self, ilks, dog, vat, dai_join):
        self.dog = dog
        self.vat = vat
        super().__init__(vat, dai_join, ilks)

    def generate_actions_for_timestep(self, t):
        actions = []
        self.open_max_vaults(actions)
        for ilk_id in self.ilks:
            ilk = self.vat.ilks[ilk_id]
            for urn in self.vat.urns[ilk_id].values():
                if Rad(urn.ink * ilk.spot) < Rad(urn.art * ilk.rate):
                    actions.append(
                        {
                            "key": "BARK",
                            "keeper": self,
                            "handler": self.dog.bark,
                            "args": [ilk_id, urn.ADDRESS, self.ADDRESS, t],
                            "kwargs": {},
                        }
                    )
        return actions


class ClipperKeeper(VaultKeeper):
    """
    clippers = {str: Clipper}
    vat = Vat
    """

    def __init__(self, vat, dai_join, ilks):
        """ ilks = [{"ilk_id": ..., "clipper": ...}]
        """

        self.clippers = {}
        for ilk in ilks:
            self.clippers[ilk["ilk_id"]] = ilk["clipper"]

        super().__init__(vat, dai_join, ilks)


class ClipperBidder(ClipperKeeper):
    """
    clippers = {str: Clipper}
    vat = Vat
    """

    def generate_actions_for_timestep(self, t):
        actions = []
        self.open_max_vaults(actions)
        self.find_and_take_sales(t, actions)
        return actions

    def find_and_take_sales(self, t, actions):
        sales_to_take = self.find_sales_to_take(t)
        for ilk_id in sales_to_take:
            for sale in sales_to_take[ilk_id]:
                stance = self.run_bidding_model(sale, ilk_id, t)
                if stance["amt"] > Wad(0):
                    actions.append(
                        {
                            "key": "TAKE",
                            "keeper": self,
                            "handler": self.clippers[ilk_id].take,
                            "args": [
                                sale.id,
                                stance["amt"],
                                stance["max_price"],
                                stance["who"],
                                stance["data"],
                                t,
                                self.ADDRESS,
                            ],
                            "kwargs": {},
                        }
                    )

    def find_sales_to_take(self, t):
        raise NotImplementedError

    def run_bidding_model(self, sale, ilk_id, t):
        raise NotImplementedError


class NaiveClipperKeeper(ClipperBidder):
    """ Takes a sale when its price is below this keeper's desired discount.
    """

    def __init__(self, vat, dai_join, ilks):
        self.desired_discounts = {}
        for ilk in ilks:
            self.desired_discounts[ilk["ilk_id"]] = ilk["desired_discount"]

        super().__init__(vat, dai_join, ilks)

    def find_sales_to_take(self, t):
        sales_to_take = {}
        for ilk_id in self.ilks:
            clipper = self.clippers[ilk_id]
            des_disc = self.desired_discounts[ilk_id]
            for sale in clipper.sales.values():
                done, price = clipper.status(sale.tic, sale.top, t)
                pip = clipper.spotter.ilks[ilk_id].pip
                val = pip.peek(t)
                if not done and price <= Ray(val / Wad(clipper.spotter.par)) * des_disc:
                    if not sales_to_take.get(ilk_id):
                        sales_to_take[ilk_id] = []
                    sales_to_take[ilk_id].append(sale)

        return sales_to_take

    def run_bidding_model(self, sale, ilk_id, t):
        stance = {}

        clipper = self.clippers[ilk_id]
        pip = clipper.spotter.ilks[ilk_id].pip
        val = pip.peek(t)
        max_price = Ray(val / Wad(clipper.spotter.par)) * self.desired_discounts[ilk_id]
        amt = Wad(
            Rad.min(Rad(sale.lot * max_price), self.vat.dai.get(self.ADDRESS, Rad(0)))
        )
        stance["max_price"] = max_price
        stance["amt"] = amt
        stance["who"] = self.ADDRESS
        stance["data"] = []

        return stance


class RedoKeeper(ClipperKeeper):
    """
    clippers = {str: Clipper}
    vat = Vat
    """

    def generate_actions_for_timestep(self, t):
        actions = []
        self.open_max_vaults(actions)
        for ilk_id in self.ilks:
            clipper = self.clippers[ilk_id]
            for sale in clipper.sales.values():
                done, _ = clipper.status(sale.tic, sale.top, t)
                if done:
                    actions.append(
                        {
                            "key": "REDO",
                            "keeper": self,
                            "handler": self.clippers[ilk_id].redo,
                            "args": [sale.id, self.ADDRESS, t],
                            "kwargs": {},
                            "extra": {"ilk_id": ilk_id,},
                        }
                    )

        return actions
