""" Experiment Module
    Class-based representation of an experiment
    (contains simulation parameters, experiment name, etc.)
"""


class Experiment:
    Cat = None
    DaiJoin = None
    Flapper = None
    Flippers = {}
    Flopper = None
    GemJoin = None
    Spotter = None
    Vat = None
    Vow = None

    Keepers = {}
    sort_keepers = None

    ilk_ids = []

    stat_trackers = []
    parameters = {}

    def __init__(
        self,
        contracts,
        keepers,
        sort_keepers,
        ilk_ids,
        Token,
        stat_trackers,
        parameters,
    ):
        """
        contracts: dict of smart contract classes, e.g. {"Cat": MyCustomCatClass}
        keepers: dict of keeper classes, e.g. {"MyCustomKeeper": MyCustomKeeperClass}
        sort_keepers: sort key used to decide the order in which keepers act each timestep
        ilk_ids: list of ilks by their ticker symbol
        Token: token class
        stat_trackers: list of methods that measure stats over the course of the experiment,
        e.g.: [num_new_kicks]
        parameters: dict of parameters used to instantiate the contracts, keepers, and simulation,
        e.g.: {"Spotter": {...}, "MyCustomKeeper": {...}, "timesteps": ...}
        """
        self.Cat = contracts["Cat"]
        self.DaiJoin = contracts["DaiJoin"]
        self.Flapper = contracts["Flapper"]
        self.Flippers = contracts["Flippers"]
        self.Flopper = contracts["Flopper"]
        self.GemJoin = contracts["GemJoin"]
        self.Spotter = contracts["Spotter"]
        self.Vat = contracts["Vat"]
        self.Vow = contracts["Vow"]

        self.Keepers = keepers
        self.sort_keepers = sort_keepers
        self.ilk_ids = ilk_ids
        self.Token = Token
        self.stat_trackers = stat_trackers
        self.parameters = parameters

    def run(self):
        # Initialize assets
        dai = self.Token("DAI")
        mkr = self.Token("MKR")
        ilks = {ilk_id: self.Token(ilk_id) for ilk_id in self.ilk_ids}

        # Initialize smart contracts
        vat = self.Vat()
        vat.file("Line", self.parameters["Vat"]["Line"])
        for ilk_id in ilks:
            vat.file_ilk(ilk_id, "line", self.parameters["Vat"][ilk_id]["line"])
            vat.file_ilk(ilk_id, "dust", self.parameters["Vat"][ilk_id]["dust"])

        spotter = self.Spotter(vat)
        spotter.file("par", self.parameters["Spotter"]["par"])

        dai_join = self.DaiJoin(vat, dai)
        gem_joins = {
            ilk_id: self.GemJoin(vat, ilk_id, ilk_token)
            for ilk_id, ilk_token in ilks.items()
        }

        flapper = self.Flapper(vat, mkr)
        flopper = self.Flopper(vat, mkr)

        vow = self.Vow(vat, flapper, flopper)
        for what in ("wait", "dump", "sump", "bump", "hump"):
            vow.file(what, self.parameters["Vow"][what])

        cat = self.Cat(vat)
        flippers = {ilk_id: self.Flippers[ilk_id](vat, cat, ilk_id) for ilk_id in ilks}
        cat.file("vow", vow)
        cat.file("box", self.parameters["Cat"]["box"])
        for ilk_id in ilks:
            cat.file_ilk(ilk_id, "chop", self.parameters["Cat"][ilk_id]["chop"])
            cat.file_ilk(ilk_id, "dunk", self.parameters["Cat"][ilk_id]["dunk"])
            cat.file_ilk(ilk_id, "flip", flippers[ilk_id])

        # Initialize keepers
        keepers = []
        for keeper_name in self.Keepers:
            Keeper = self.Keepers[keeper_name]
            amount = self.parameters["Keepers"][keeper_name]["amount"]
            keeper_ilks = [
                {
                    "c_ratio": self.parameters["Keepers"][keeper_name]["c_ratio"],
                    "flipper": flippers[ilk_id],
                    "gem_join": gem_joins[ilk_id],
                    "ilk_id": ilk_id,
                    "token": ilks[ilk_id],
                }
                for ilk_id in ilks
            ]
            for _ in range(amount):
                keeper = Keeper(vat, dai_join, keeper_ilks)
                keepers.append(keeper)

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
            "keepers": keepers,
            "spotter": spotter,
            "stats": {},
            "vat": vat,
            "vow": vow,
        }

        # Run simulation
        for t in range(self.parameters["timesteps"]):
            for track_stat in self.stat_trackers:
                track_stat(state, {"key": "T_START"})

            # Execute keeper actions in the specified order
            for keeper in sorted(keepers, self.sort_keepers):
                actions = keeper.execute_actions_for_timestep(t)
                for action in actions:
                    for track_stat in self.stat_trackers:
                        track_stat(state, action)

            for track_stat in self.stat_trackers:
                track_stat(state, {"key": "T_END"})

            # TODO: Stream back stats
            # For now: write to file
