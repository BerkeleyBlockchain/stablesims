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
    GemJoins = {}
    Spotter = None
    Vat = None
    Vow = None

    Keepers = {}
    sort_keepers = None

    ilks = []
    dai = None

    stats = None
    parameters = {}

    def __init__(
        self, contracts, keepers, sort_keepers, ilks, dai, mkr, stats, parameters,
    ):
        self.Cat = contracts["Cat"]
        self.DaiJoin = contracts["DaiJoin"]
        self.Flapper = contracts["Flapper"]
        self.Flippers = contracts["Flippers"]
        self.Flopper = contracts["Flopper"]
        self.GemJoins = contracts["GemJoins"]
        self.Spotter = contracts["Spotter"]
        self.Vat = contracts["Vat"]
        self.Vow = contracts["Vow"]

        self.Keepers = keepers
        self.sort_keepers = sort_keepers
        self.ilks = ilks
        self.dai = dai
        self.mkr = mkr
        self.stats = stats
        self.parameters = parameters

    def run(self):
        # Initialize assets
        dai = self.dai("Dai", "DAI")
        mkr = self.mkr("Maker", "MKR")
        ilks = {ilk_id: Token(ilk_id) for ilk_id, Token in self.ilks}

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
            ilk_id: self.GemJoins[ilk_id](vat, ilk_id, ilk_token)
            for ilk_id, ilk_token in ilks.items()
        }

        flapper = self.Flapper(vat, mkr)
        flopper = self.Flopper(vat, mkr)

        vow = self.Vow(vat, flapper, flopper)
        for what in ("wait", "bump", "sump", "dump", "hump"):
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
            Keeper = self.Keepers[keeper_name]["Keeper"]
            amount = self.Keepers[keeper_name]["amount"]
            keeper_ilks = [
                {"gem_join": gem_joins[ilk_id], "flipper": flippers[ilk_id]}
                for ilk_id in ilks
            ]
            keepers.extend([Keeper(vat, dai_join, keeper_ilks) for _ in range(amount)])

        # Run simulation
        for _t in range(self.parameters["timesteps"]):
            for keeper in sorted(keepers, self.sort_keepers):
                keeper.execute_action_for_timestep()
            # Record data
