""" Extension of the experiment module using the Dutch Auction system.
"""

import csv
from copy import deepcopy
import matplotlib.pyplot as plt

from pydss.pymaker.numeric import Wad, Rad, Ray
from pydss.util import RequireException
from experiments.experiment import Experiment


class DutchAuctionsExperiment(Experiment):
    """ Experiment engine fit for the set of contracts in Maker's
        liquidations 2.0 system.
    """

    def file_contracts(self, contracts):
        self.Abacus = contracts["Abacus"]
        self.Clipper = contracts["Clipper"]
        self.DaiJoin = contracts["DaiJoin"]
        self.Dog = contracts["Dog"]
        self.Flapper = contracts["Flapper"]
        self.Flopper = contracts["Flopper"]
        self.GemJoin = contracts["GemJoin"]
        self.Spotter = contracts["Spotter"]
        self.Vat = contracts["Vat"]
        self.Vow = contracts["Vow"]
        self.Uniswap = contracts["Uniswap"]
        self.GasOracle = contracts["GasOracle"]

    def run(self, sim_name, filename, fieldnames):
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

        gas_oracle = self.GasOracle(self.parameters["GasOracle"]["price_feed_file"])
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

        calc = self.Abacus()
        for what in self.parameters["Abacus"]:
            calc.file(what, self.parameters["Abacus"][what])

        dog = self.Dog(vat)
        dog.file("vow", vow)
        dog.file("Hole", self.parameters["Dog"]["Hole"])
        for ilk_id in ilks:
            dog.file_ilk(ilk_id, "chop", self.parameters["Dog"][ilk_id]["chop"])
            dog.file_ilk(ilk_id, "hole", self.parameters["Dog"][ilk_id]["hole"])

        clippers = {}
        for ilk_id in ilks:
            clipper = self.Clipper(vat, spotter, dog, ilk_id)
            dog.file_ilk(ilk_id, "clip", clipper)
            clipper.file("buf", self.parameters["Clipper"][ilk_id]["buf"])
            clipper.file("tail", self.parameters["Clipper"][ilk_id]["tail"])
            clipper.file("cusp", self.parameters["Clipper"][ilk_id]["cusp"])
            clipper.file("chip", self.parameters["Clipper"][ilk_id]["chip"])
            clipper.file("tip", self.parameters["Clipper"][ilk_id]["tip"])
            clipper.file_address("vow", vow)
            clipper.file_address("calc", calc)
            clippers[ilk_id] = clipper

        uniswap = self.Uniswap(self.parameters["Uniswap"]["pairs"])

        # Initialize state
        state = {
            "t": 0,
            "calc": calc,
            "clippers": clippers,
            "dai": dai,
            "dai_join": dai_join,
            "dog": dog,
            "flapper": flapper,
            "flopper": flopper,
            "gem_joins": gem_joins,
            "ilks": ilks,
            "spotter": spotter,
            "stats": {},
            "vat": vat,
            "vow": vow,
            "uniswap": uniswap,
            "gas_oracle": gas_oracle,
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
            state["t"] = t
            for track_stat in self.stat_trackers:
                track_stat(state, {"key": "T_START"}, [])

            actions_t = []
            for keeper_name in state["keepers"]:
                for keeper in state["keepers"][keeper_name]:
                    actions_t.extend(keeper.generate_actions_for_timestep(t))

            for action in sorted(actions_t, key=self.sort_actions):
                try:
                    results = action["handler"](*action["args"], **action["kwargs"])
                except RequireException:
                    continue
                for track_stat in self.stat_trackers:
                    track_stat(state, action, results or [])

            for track_stat in self.stat_trackers:
                track_stat(state, {"key": "T_END"}, [])

            historical_stats.append(deepcopy(state["stats"]))
            self.write_csv(fieldnames, filename, state["stats"])

        time_range = list(range(self.parameters["timesteps"]))
        fig = plt.figure(figsize=(6,6))
        axs = fig.subplots(5)
        fig.suptitle(f"Timeframe: {sim_name.split('_')[1]}, Chip: {float(state['clippers']['WETH'].chip)}, Tip: {float(state['clippers']['WETH'].tip)}")
        fig.tight_layout(pad=2, h_pad=2)
        axs[0].plot(time_range, [stats["WETH_price"] for stats in historical_stats])
        axs[0].title.set_text("ETH price ($)")
        axs[1].plot(time_range, [stats["gas_price_gwei"] for stats in historical_stats])
        axs[1].title.set_text("Gas price (Gwei)")
        axs[2].plot(time_range, [stats["num_new_barks"] for stats in historical_stats])
        axs[2].title.set_text("Number of liquidations")
        axs[3].plot(time_range, [stats["num_unsafe_vaults"] for stats in historical_stats])
        axs[3].title.set_text("Number of unsafe vaults")
        axs[4].plot(time_range, [stats["incentive_amount"] for stats in historical_stats])
        axs[4].title.set_text("Incentive amount paid ($)")
        plt.savefig(f"/bab-stablesims/experiments/dutch_auctions/results/05-19-2021/{sim_name}.png")

    def write_csv(self, fieldnames, filename, data):
        """ Write stats to one csv with the name field indicating which sim was run
        """
        with open(filename, mode="a") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            stats = self.format_data(data, fieldnames)
            print(data)
            writer.writerow(stats)

    def format_data(self, state, fieldnames, full_state=True):
        data = state if full_state else state["stats"]
        data = deepcopy(data)
        for key, value in data.items():
            if key in fieldnames:
                if isinstance(value, (Ray, Rad, Wad)):
                    data[key] = float(value)
                elif isinstance(value, dict):
                    data[key] = self.format_data(value)
                elif hasattr(value, "__iter__"):
                    data[key] = list(map(self.format_data, value))

        return data
