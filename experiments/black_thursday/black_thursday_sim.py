""" Black Thursday base experiment.
"""


import random

from experiments.experiment import Experiment
from experiments.stats import (
    ilk_price,
    num_new_bites,
    num_bids_placed,
    num_active_bids,
    keeper_gem_balances,
)
from pydss.cat import Cat
from pydss.join import DaiJoin, GemJoin
from pydss.spot import Spotter, PipLike
from pydss.flip import Flipper
from pydss.vat import Vat
from pydss.vow import Vow
from pydss.token import Token
from pydss.pymaker.numeric import Wad, Rad, Ray
from pydss.keeper import (
    NaiveFlipperKeeper,
    PatientFlipperKeeper,
    SpotterKeeper,
    BiteKeeper,
    NaiveVaultKeeper,
)


contracts = {
    "Cat": Cat,
    "DaiJoin": DaiJoin,
    "Flapper": None,
    "Flipper": Flipper,
    "Flopper": None,
    "GemJoin": GemJoin,
    "Spotter": Spotter,
    "Vat": Vat,
    "Vow": Vow,
}
keepers = {
    "NaiveVaultKeeper": NaiveVaultKeeper,
    "NaiveFlipperKeeper": NaiveFlipperKeeper,
    "PatientFlipperKeeper": PatientFlipperKeeper,
    "SpotterKeeper": SpotterKeeper,
    "BiteKeeper": BiteKeeper,
}
sort_actions = lambda _: random.random()
ilk_ids = ["ETH"]
stat_trackers = [
    ilk_price("ETH"),
    num_new_bites(),
    num_bids_placed(),
    keeper_gem_balances(),
    num_active_bids(),
]
parameters = {
    "Cat": {
        "box": Rad(15000000000000000000000000000000000000000000000000000),
        "ETH": {
            "chop": Wad(1130000000000000000),
            "dunk": Rad(50000000000000000000000000000000000000000000000000),
        },
    },
    "Flipper": {"ETH": {"beg": Wad(1050000000000000000), "ttl": 18, "tau": 288,}},
    "Keepers": {
        "NaiveVaultKeeper": {
            "amount": 500,
            "get_params": lambda state: [
                state["vat"],
                state["dai_join"],
                [
                    {
                        "ilk_id": "ETH",
                        "token": state["ilks"]["ETH"],
                        "init_balance": random.gauss(10, 2.155),
                        "gem_join": state["gem_joins"]["ETH"],
                        "c_ratio": random.gauss(1.5, 0.216),
                    }
                ],
            ],
        },
        "NaiveFlipperKeeper": {
            "amount": 5,
            "get_params": lambda state: [
                state["vat"],
                state["dai_join"],
                [
                    {
                        "ilk_id": "ETH",
                        "token": state["ilks"]["ETH"],
                        "init_balance": random.gauss(250, 64.655),
                        "gem_join": state["gem_joins"]["ETH"],
                        "c_ratio": random.gauss(2, 0.216),
                        "flipper": state["flippers"]["ETH"],
                    }
                ],
            ],
        },
        "PatientFlipperKeeper": {
            "amount": 1,
            "get_params": lambda state: [
                state["vat"],
                state["dai_join"],
                [
                    {
                        "ilk_id": "ETH",
                        "token": state["ilks"]["ETH"],
                        "init_balance": 500,
                        "gem_join": state["gem_joins"]["ETH"],
                        "c_ratio": random.gauss(2, 0.216),
                        "flipper": state["flippers"]["ETH"],
                    }
                ],
                state["keepers"]["NaiveFlipperKeeper"],
            ],
        },
        "SpotterKeeper": {
            "amount": 1,
            "get_params": lambda state: [
                [{"ilk_id": "ETH", "token": state["ilks"]["ETH"], "init_balance": 0}],
                state["spotter"],
            ],
        },
        "BiteKeeper": {
            "amount": 1,
            "get_params": lambda state: [
                [{"ilk_id": "ETH", "token": state["ilks"]["ETH"], "init_balance": 0}],
                state["cat"],
                state["vat"],
            ],
        },
    },
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

BlackThursday = Experiment(
    contracts, keepers, sort_actions, ilk_ids, Token, stat_trackers, parameters
)
