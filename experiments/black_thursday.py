""" Black Thursday base experiment.
"""


import random

from experiments.experiment import Experiment
from pydss.cat import Cat
from pydss.join import DaiJoin, GemJoin
from pydss.spotter import Spotter
from pydss.vat import Vat
from pydss.vow import Vow
from pydss.token import Token
from pydss.pymaker.numeric import Wad, Rad
from pydss.stats import ilk_price, num_new_bites, num_new_bids, keeper_balances

contracts = {
    "Cat": Cat,
    "DaiJoin": DaiJoin,
    "Flapper": None,
    "Flippers": {"FlipperEth": None},
    "Flopper": None,
    "GemJoin": GemJoin,
    "Spotter": Spotter,
    "Vat": Vat,
    "Vow": Vow,
}
keepers = {"NaiveFlipperKeeper": None}
sort_keepers = random.random()
ilk_ids = ["ETH"]
stat_trackers = [ilk_price("ETH"), num_new_bites(), num_new_bids(), keeper_balances()]
parameters = {
    "Cat": {
        "box": Rad(15000000000000000000000000000000000000000000000000000),
        "ETH": {
            "chop": Wad(1130000000000000000),
            "dunk": Rad(50000000000000000000000000000000000000000000000000),
        },
    },
    "Keepers": {"NaiveFlipperKeeper": {"amount": 1000}},
    "Spotter": {"par": 1},
    "timesteps": 144,
    "Vat": {
        "Line": Rad(1621230562029182607785180351895167282074137639278363742),
        "ETH": {
            "line": Rad(590000000000000000000000000000000000000000000000000000),
            "dust": Rad(500000000000000000000000000000000000000000000000),
        },
    },
    "Vow": {
        "wait": 561600,
        "dump": Wad(250000000000000000000),
        "sump": Rad(50000000000000000000000000000000000000000000000000),
        "bump": Rad(10000000000000000000000000000000000000000000000000),
        "hump": Rad(4000000000000000000000000000000000000000000000000000),
    },
}

BlackThursday = Experiment(
    contracts, keepers, sort_keepers, ilk_ids, Token, stat_trackers, parameters
)
