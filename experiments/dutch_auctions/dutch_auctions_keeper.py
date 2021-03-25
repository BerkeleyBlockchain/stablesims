""" Dutch Auctions Keeper Module
    Extension of the Keeper module which accomodates the new
    Dutch auction liquidation system.
"""

from pydss.keeper import Keeper, VaultKeeper
from pydss.pymaker.numeric import Rad


class BarkKeeper(Keeper):
    """
    dog = Dog
    vat = Vat
    """

    def __init__(self, ilks, dog, vat):
        self.dog = dog
        self.vat = vat
        super().__init__(ilks)

    def generate_actions_for_timestep(self, t):
        actions = []
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
    """

    def __init__(self, vat, dai_join, ilks):
        """ ilks = [{"ilk_id": ..., "clipper": ...}]
        """

        self.clippers = {}
        for ilk in ilks:
            self.clippers[ilk["ilk_id"]] = ilk["clipper"]

        super().__init__(vat, dai_join, ilks)

    def generate_actions_for_timestep(self, t):
        actions = []
        self.open_max_vaults(actions)
        self.find_and_take_sales(t, actions)
        return actions

    def find_and_take_sales(self, t, actions):
        sales_to_take = self.find_sales_to_take(t)
        for ilk_id in sales_to_take:
            for sale in sales_to_take[ilk_id]:
                stance = self.run_bidding_model(sale, ilk_id)
                if stance:
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

    def run_bidding_model(self, sale, ilk_id):
        raise NotImplementedError


class NaiveClipperKeeper(ClipperKeeper):
    """ Takes a sale when its price is below this keeper's desired discount.
    """

    def find_sales_to_take(self, t):
        pass

    def run_bidding_model(self, sale, ilk_id):
        pass
