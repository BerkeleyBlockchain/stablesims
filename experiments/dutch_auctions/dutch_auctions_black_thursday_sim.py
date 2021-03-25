""" Black Thursday experiment using Dutch Auctions.
"""

import random

from experiments.dutch_auctions.dutch_auctions_experiment import DutchAuctionExperiment
from experiments.dutch_auctions.abaci import LinearDecrease
from experiments.dutch_auctions.clip import Clipper
from experiments.dutch_auctions.dog import Dog
from pydss.join import DaiJoin, GemJoin
from pydss.spot import Spotter, PipLike
from pydss.vat import Vat
from pydss.vow import Vow
from pydss.token import Token
from pydss.pymaker.numeric import Wad, Rad, Ray


contracts = {
    "Abacus": LinearDecrease,
    "Clipper": Clipper,
    "DaiJoin": DaiJoin,
    "Dog": Dog,
    "Flapper": None,
    "Flopper": None,
    "GemJoin": GemJoin,
    "Spotter": Spotter,
    "Vat": Vat,
    "Vow": Vow,
}
keepers = {}
sort_actions = lambda _: random.random()
ilk_ids = ["ETH"]
stat_trackers = []
parameters = {
    "Abacus": {"tau": 172800},
    "Clipper": {
        "ETH": {
            "buf": Ray.from_number(1.5),
            "tail": 172800,
            "cusp": Ray.from_number(0.5),
            "chip": Wad.from_number(0.08),
            "tip": Rad(0),
        }
    },
    "Dog": {"Hole": Rad(15000000000000000000000000000000000000000000000000000)},
    "Keepers": {},
    "Spotter": {
        "par": Ray(1000000000000000000000000000),
        "ETH": {
            "pip": PipLike("price_feeds/eth_black_thursday_10min.json"),
            "mat": Wad(1500000000000000000),
        },
    },
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

DutchAuctionsBlackThursday = DutchAuctionExperiment(
    contracts, keepers, sort_actions, ilk_ids, Token, stat_trackers, parameters
)
