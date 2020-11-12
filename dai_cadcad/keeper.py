""" Keeper Module
    Class-based representation of a keeper in the Maker ecosystem.
    By this, we mean any external agent, not just auction keepers.
    (contains only what is necessary for the simulation)
"""

from uuid import uuid4

from dai_cadcad.pymaker.numeric import Wad, Rad  # , Ray

# from dai_cadcad.util import require


class Keeper:
    ADDRESS = ""

    vat = None
    dai_join = None

    # The collateral balances held by this Keeper outside of the Maker Protocol.
    ilks = {}
    # The ERC-20 DAI balance held by this Keeper
    dai = Rad(0)
    # The CDPs held by this Keeper (same ID used for urn, gem, & dai addresses)
    cdps = {}

    def __init__(self, ilks, vat, dai_join):
        """ `ilks` must be an array containing a configuration abject for each ilk type of the
            following form:
                {
                    "ilk_id": str,
                    "gem": Wad,
                    "flip": Flipper,
                    "join" GemJoin,
                }
        """

        self.ADDRESS = uuid4().hex

        self.vat = vat
        self.dai_join = dai_join

        for ilk in ilks:
            self.cdps[ilk["ilk_id"]] = []
            self.ilks[ilk["ilk_id"]] = {
                "gem": ilk["gem"],
                "flip": ilk["flip"],
                "join": ilk["join"],
            }

    def open_vault(self, ilk_id, gem, dai):
        cdp_id = uuid4().hex
        # TOOD: Make the `GemJoin` contract handle checking that this Keeper has enough `gem`.
        # TODO: Have the `join` method expect the sender address instead of `msg.sender`
        self.ilks[ilk_id]["join"].join(self.ADDRESS, cdp_id, gem)
        self.cdps[ilk_id].append(cdp_id)
        self.vat.frob(ilk_id, cdp_id, cdp_id, cdp_id, gem, dai)

    def close_vault(self, ilk_id, cdp_id):
        dink = Wad(0) - self.vat.urns[ilk_id][cdp_id]["ink"]
        dart = Wad(0) - self.vat.urns[ilk_id][cdp_id]["art"]
        self.vat.frob(ilk_id, cdp_id, cdp_id, cdp_id, dink, dart)
        self.ilks[ilk_id]["join"].exit(self.ADDRESS, cdp_id, Wad(0) - dink)
