""" Experiment Module
    Class-based representation of an experiment
    (contains simulation parameters, experiment name, etc.)
"""

from copy import deepcopy
import matplotlib.pyplot as plt
from pydss.pymaker.numeric import Wad, Rad, Ray
from pydss.util import RequireException


class Experiment:
    """
    Cat = Cat
    DaiJoin = DaiJoin
    Flapper = Flapper
    Flippers = dict[str: Flipper]
    Flopper = Flopper
    GemJoin = GemJoin
    Spotter = Spotter
    Vat = Vat
    Vow = Vow

    Keepers = dict[str: Keeper]
    sort_actions = function

    ilk_ids = list[str]

    stat_trackers = list[function]
    parameters = dict
    """

    def __init__(
        self,
        contracts,
        keepers,
        sort_actions,
        ilk_ids,
        Token,
        stat_trackers,
        parameters,
    ):
        """
        contracts: dict of smart contract classes, e.g. {"Cat": MyCustomCatClass}
        keepers: dict of keeper classes, e.g. {"MyCustomKeeper": MyCustomKeeperClass}
        sort_actions: sort key used to decide the order in which keepers act each timestep
        ilk_ids: list of ilks by their ticker symbol
        Token: token class
        stat_trackers: list of methods that measure stats over the course of the experiment,
        e.g.: [num_new_kicks]
        parameters: dict of parameters used to instantiate the contracts, keepers, and simulation,
        e.g.: {"Spotter": {...}, "MyCustomKeeper": {...}, "timesteps": ...}
        """
        self.file_contracts(contracts)

        self.Keepers = keepers
        self.sort_actions = sort_actions
        self.ilk_ids = ilk_ids
        self.Token = Token
        self.stat_trackers = stat_trackers
        self.parameters = parameters

    def file_contracts(self, contracts):
        self.Cat = contracts["Cat"]
        self.DaiJoin = contracts["DaiJoin"]
        self.Flapper = contracts["Flapper"]
        self.Flipper = contracts["Flipper"]
        self.Flopper = contracts["Flopper"]
        self.GemJoin = contracts["GemJoin"]
        self.Spotter = contracts["Spotter"]
        self.Vat = contracts["Vat"]
        self.Vow = contracts["Vow"]
        self.Uniswap = contracts["Uniswap"]

    def run(self):
        # Initialize assets
        dai = self.Token("DAI")
        # mkr = self.Token("MKR")
        ilks = {ilk_id: self.Token(ilk_id) for ilk_id in self.ilk_ids}

        # Initialize smart contracts
        vat = self.Vat()
        vat.file("Line", self.parameters["Vat"]["Line"])
        for ilk_id in ilks:
            vat.init(ilk_id)
            vat.file_ilk(ilk_id, "line", self.parameters["Vat"][ilk_id]["line"])
            vat.file_ilk(ilk_id, "dust", self.parameters["Vat"][ilk_id]["dust"])

        spotter = self.Spotter(vat)
        spotter.file("par", self.parameters["Spotter"]["par"])
        for ilk_id in ilks:
            spotter.file_ilk(ilk_id, "pip", self.parameters["Spotter"][ilk_id]["pip"])
            spotter.file_ilk(ilk_id, "mat", self.parameters["Spotter"][ilk_id]["mat"])

        dai_join = self.DaiJoin(vat, dai)
        gem_joins = {
            ilk_id: self.GemJoin(vat, ilk_id, ilk_token)
            for ilk_id, ilk_token in ilks.items()
        }

        # flapper = self.Flapper(vat, mkr)
        # flopper = self.Flopper(vat, mkr)
        flapper = None
        flopper = None

        vow = self.Vow(vat, flapper, flopper)
        for what in ("wait", "dump", "sump", "bump", "hump"):
            vow.file(what, self.parameters["Vow"][what])

        cat = self.Cat(vat)
        cat.file("vow", vow)
        cat.file("box", self.parameters["Cat"]["box"])

        flippers = {}
        for ilk_id in ilks:
            flipper = self.Flipper(vat, cat, ilk_id,)
            flipper.file("beg", self.parameters["Flipper"][ilk_id]["beg"])
            flipper.file("ttl", self.parameters["Flipper"][ilk_id]["ttl"])
            flipper.file("tau", self.parameters["Flipper"][ilk_id]["tau"])
            flippers[ilk_id] = flipper

            cat.file_ilk(ilk_id, "chop", self.parameters["Cat"][ilk_id]["chop"])
            cat.file_ilk(ilk_id, "dunk", self.parameters["Cat"][ilk_id]["dunk"])
            cat.file_ilk(ilk_id, "flip", flipper)

        uniswap = self.Uniswap(self.parameters["Uniswap"]["pairs"])

        # Initialize state
        state = {
            "cat": cat,
            "dai": dai,
            "dai_join": dai_join,
            "flapper": flapper,
            "flippers": flippers,
            "flopper": flopper,
            "gem_joins": gem_joins,
            "ilks": ilks,
            "spotter": spotter,
            "stats": {},
            "vat": vat,
            "vow": vow,
            "uniswap": uniswap,
        }

        # Initialize keepers
        state["keepers"] = {keeper_name: [] for keeper_name in self.Keepers}
        for keeper_name in self.Keepers:
            Keeper = self.Keepers[keeper_name]
            amount = self.parameters["Keepers"][keeper_name]["amount"]
            for _ in range(amount):
                keeper_params = self.parameters["Keepers"][keeper_name]["get_params"](
                    state
                )
                state["keepers"][keeper_name].append(Keeper(*keeper_params))

        # Run simulation
        historical_stats = []
        for t in range(self.parameters["timesteps"]):
            for track_stat in self.stat_trackers:
                track_stat(state, {"key": "T_START"}, [])

            actions_t = []
            for keeper_name in state["keepers"]:
                for keeper in state["keepers"][keeper_name]:
                    actions_t.extend(keeper.generate_actions_for_timestep(t))

            for action in sorted(actions_t, key=self.sort_actions):
                try:
                    results = action["handler"](*action["args"], **action["kwargs"])
                    results = list(results) if results else []
                except RequireException:
                    continue
                for track_stat in self.stat_trackers:
                    track_stat(state, action, results)

            for track_stat in self.stat_trackers:
                track_stat(state, {"key": "T_END"}, [])

            historical_stats.append(deepcopy(state["stats"]))

        _, axs = plt.subplots(4)
        time_range = list(range(self.parameters["timesteps"]))
        axs[0].plot(
            time_range, [stats["ilk_price"]["WETH"] for stats in historical_stats]
        )
        axs[1].plot(time_range, [stats["num_new_bites"] for stats in historical_stats])
        axs[2].plot(
            time_range, [stats["num_bids_placed"] for stats in historical_stats]
        )
        axs[3].plot(time_range, [stats["auction_debt"] for stats in historical_stats])
        plt.show()
        # self.write(
        #     datetime.now().strftime("Experiment %d-%m-%Y at %H.%M.%S.txt"), state, t
        # )

    def format_data(self, state, full_state=True):
        data = state if full_state else state["stats"]
        data = deepcopy(data)
        for key, value in data.items():
            if isinstance(value, (Ray, Rad, Wad)):
                data[key] = float(data[value])
            elif isinstance(value, dict):
                data[key] = self.format_data(value)
            elif hasattr(value, "__iter__"):
                data[key] = list(map(self.format_data, value))

        return data

    def write(self, filename, data, t):
        with open(filename, "a") as f:
            f.write("==================\n")
            f.write("Timestep: {}".format(t))
            f.write(self.format_data(data) + "\n")
