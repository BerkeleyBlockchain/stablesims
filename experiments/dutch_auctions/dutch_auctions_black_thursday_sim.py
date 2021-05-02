""" Black Thursday experiment using Dutch Auctions.
"""

import random

from experiments.dutch_auctions.dutch_auctions_experiment import DutchAuctionExperiment
from experiments.dutch_auctions.abaci import LinearDecrease
from experiments.dutch_auctions.clip import Clipper
from experiments.dutch_auctions.dog import Dog
from experiments.dutch_auctions.dutch_auctions_keeper import (
    BarkKeeper,
    NaiveClipperKeeper,
    RedoKeeper,
)
from experiments.dutch_auctions.dutch_auctions_stats import (
    num_new_barks,
    num_sales_taken,
)
from experiments.stats import ilk_price, keeper_gem_balances
from pydss.join import DaiJoin, GemJoin
from pydss.spot import Spotter, PipLike
from pydss.vat import Vat
from pydss.vow import Vow
from pydss.token import Token
from pydss.uniswap import Uniswap
from pydss.pymaker.numeric import Wad, Rad, Ray
from pydss.keeper import NaiveVaultKeeper, SpotterKeeper


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
    "Uniswap": Uniswap,
}
keepers = {
    "NaiveVaultKeeper": NaiveVaultKeeper,
    "NaiveClipperKeeper": NaiveClipperKeeper,
    "RedoKeeper": RedoKeeper,
    "BarkKeeper": BarkKeeper,
    "SpotterKeeper": SpotterKeeper,
}
sort_actions = lambda _: random.random()
ilk_ids = ["WETH"]
stat_trackers = [
    num_new_barks(),
    num_sales_taken(),
    keeper_gem_balances(),
    ilk_price("WETH"),
]
parameters = {
    "Abacus": {"tau": 72},
    "Clipper": {
        "WETH": {
            "buf": Ray.from_number(1.05),
            "tail": 72,
            "cusp": Ray.from_number(0.5),
            "chip": Wad.from_number(0.08),
            "tip": Rad(0),
        }
    },
    "Dog": {
        "Hole": Rad(15000000000000000000000000000000000000000000000000000),
        "WETH": {
            "chop": Wad.from_number(1.13),
            "hole": Rad(15000000000000000000000000000000000000000000000000000),
        },
    },
    "Keepers": {
        "NaiveVaultKeeper": {
            "amount": 50,
            "get_params": lambda state: [
                state["vat"],
                state["dai_join"],
                [
                    {
                        "ilk_id": "WETH",
                        "token": state["ilks"]["WETH"],
                        "init_balance": random.gauss(10, 2.155),
                        "gem_join": state["gem_joins"]["WETH"],
                        "spot_padding": Wad.from_number(random.gauss(12 / 14, 0.216)),
                    }
                ],
                state["uniswap"],
            ],
        },
        "NaiveClipperKeeper": {
            "amount": 5,
            "get_params": lambda state: [
                state["vat"],
                state["dai_join"],
                [
                    {
                        "ilk_id": "WETH",
                        "token": state["ilks"]["WETH"],
                        "init_balance": random.gauss(25, 6.466),
                        "gem_join": state["gem_joins"]["WETH"],
                        "spot_padding": Wad.from_number(random.gauss(12 / 14, 0.216)),
                        "clipper": state["clippers"]["WETH"],
                        "desired_discount": Ray.from_number(random.gauss(0.85, 0.061)),
                    }
                ],
                state["uniswap"],
            ],
        },
        "RedoKeeper": {
            "amount": 5,
            "get_params": lambda state: [
                state["vat"],
                state["dai_join"],
                [
                    {
                        "ilk_id": "WETH",
                        "token": state["ilks"]["WETH"],
                        "init_balance": random.gauss(25, 6.466),
                        "gem_join": state["gem_joins"]["WETH"],
                        "spot_padding": Wad.from_number(random.gauss(12 / 14, 0.216)),
                        "clipper": state["clippers"]["WETH"],
                    }
                ],
                state["uniswap"],
            ],
        },
        "SpotterKeeper": {
            "amount": 1,
            "get_params": lambda state: [
                [{"ilk_id": "WETH", "token": state["ilks"]["WETH"], "init_balance": 0}],
                state["spotter"],
            ],
        },
        "BarkKeeper": {
            "amount": 5,
            "get_params": lambda state: [
                [
                    {
                        "ilk_id": "WETH",
                        "token": state["ilks"]["WETH"],
                        "init_balance": random.gauss(100, 2.155),
                        "gem_join": state["gem_joins"]["WETH"],
                        "spot_padding": Wad.from_number(random.gauss(12 / 14, 0.216)),
                    }
                ],
                state["dog"],
                state["vat"],
                state["dai_join"],
                state["uniswap"],
            ],
        },
    },
    "Spotter": {
        "par": Ray(1000000000000000000000000000),
        "WETH": {
            "pip": PipLike("price_feeds/eth_black_thursday_10min.json"),
            "mat": Wad(1500000000000000000),
        },
    },
    "timesteps": 144,
    "Vat": {
        "Line": Rad(1621230562029182607785180351895167282074137639278363742),
        "WETH": {
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
    "Uniswap": {
        "pairs": {
            "0xa478c2975ab1ea89e8196811f51a7b7ade33eb11": {
                "path": "",  # No liquidity data for Black Thursday
                "token0": "DAI",
                "token1": "WETH",
            }
        }
    },
}

DutchAuctionsBlackThursday = DutchAuctionExperiment(
    contracts, keepers, sort_actions, ilk_ids, Token, stat_trackers, parameters
)
