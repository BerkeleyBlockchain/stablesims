""" Keeper Module
    Class-based representation of a keeper in the Maker ecosystem.
    By this, we mean any external agent, not just auction keepers.
    (contains only what is necessary for the simulation)
"""

from uuid import uuid4

from dai_cadcad.pymaker.numeric import Wad  # , Rad, Ray

# from dai_cadcad.util import require


class Keeper:
    ADDRESS = ""

    vat = None
    dai_join = None
    gem_joins = {}
    flippers = {}

    urns = {}
    num_urns = 0

    def __init__(self, vat, dai_join, ilks):

        self.ADDRESS = f"keeper-{uuid4().hex}"

        self.vat = vat
        self.dai_join = dai_join

        for ilk in ilks:
            self.gem_joins[ilk["ilk_id"]] = ilk["gem_join"]
            self.flippers[ilk["ilk_id"]] = ilk["flipper"]

    def generate_urn_key(self):
        urn_key = f"urn-{self.num_urns}-{self.ADDRESS}"
        self.num_urns += 1
        return urn_key

    def open_vault(self, ilk_id, dink, dart):
        urn_key = self.generate_urn_key()
        self.urns[urn_key] = ilk_id
        # Lock collateral into the system
        self.gem_joins[ilk_id].join(self.ADDRESS, self.ADDRESS, dink)
        # Create a vault with the locked collateral
        # `vat.gem` and `vat.dai` use the Keeper's address, while `vat.urns` uses `urn_key`
        self.vat.frob(ilk_id, urn_key, self.ADDRESS, self.ADDRESS, dink, dart)
        # TODO: Ensure that `vat.move` can create a recipient address if it doesn't exist
        # Move in-system DAI from the urn address to the keeper address
        self.vat.move(urn_key, self.ADDRESS)

    def close_vault(self, urn_key):
        ilk_id = self.urns[urn_key]
        dink = Wad(0) - self.vat.urns[ilk_id][urn_key]["ink"]
        dart = Wad(0) - self.vat.urns[ilk_id][urn_key]["art"]
        # Zero out the vault, freeing collateral
        self.vat.frob(ilk_id, urn_key, self.ADDRESS, self.ADDRESS, dink, dart)
        # Withdraw freed collateral
        self.gem_joins[ilk_id].exit(self.ADDRESS, self.ADDRESS, Wad(0) - dink)
        del self.urns[urn_key]

    # def keeper_bid_flipper_eth(
    #     self, flipper, vat, spotter, stance, bid_id, user_id, now, stats
    # ):
    #     # TODO: Reference flipper_dent, flipper_tend, maybe as instance variables or import

    #     bid = flipper["bids"][bid_id]

    #     if stance and (
    #         "gas_price" not in stance
    #         or spotter["ilks"]["gas"]["val"] <= stance["gas_price"]
    #     ):
    #         price = stance["price"]

    #         if bid["bid"] == bid["tab"]:
    #             # Dent phase
    #             our_lot = Wad(bid["bid"] / Rad(price))
    #             if (
    #                 our_lot * flipper["beg"] <= bid["lot"]
    #                 and our_lot < bid["lot"]
    #                 and vat["dai"][user_id] >= bid["bid"]
    #             ):
    #                 flipper_dent(
    #                     flipper, vat, bid_id, user_id, our_lot, bid["bid"], now
    #                 )
    #                 stats["num_bids"] += 1

    #         else:
    #             # Tend phase
    #             our_bid = Rad.min(Rad(bid["lot"]) * price, bid["tab"])
    #             if (
    #                 (our_bid >= bid["bid"] * flipper["beg"] or our_bid == bid["tab"])
    #                 and our_bid > bid["bid"]
    #                 and vat["dai"][user_id]
    #                 >= (our_bid if user_id != bid["guy"] else our_bid - bid["bid"])
    #             ):
    #                 flipper_tend(
    #                     flipper, vat, bid_id, user_id, bid["lot"], our_bid, now
    #                 )
    #                 stats["num_bids"] += 1
