""" Experiment Module
    Class-based representation of an experiment
    (contains simulation parameters, experiment name, etc.)
"""

# from cadCAD.engine import ExecutionContext, ExecutionMode, Executor
# from cadCAD import configuration
# from cadCAD import configs


class Experiment:
    vat = None
    vow = None
    cat = None
    flippers = {}
    flapper = None
    flopper = None
    spotter = None
    gem_joins = {}
    dai_join = None
    sim_params = {}

    def __init__(
        self,
        ilks,
        vat_params,
        vow_params,
        cat_params,
        spotter_params,
        dai_join_params,
        gem_join_params,
        dispatchers,
        loggers,
        action_sort_key,
    ):
        """ `ilks` must be an array containing a configuration abject for each ilk type of the
            following form:
            {
                "ilk_id": str,
                "cat_params": {
                    "flip": Flipper,
                    "chop": Wad,
                    "dunk": Rad
                },
                "spotter_params": {
                    "pip": PipLike,
                    "mat": Ray
                },
                "gem_join_params": {
                    "gem": Token
                },
                "vat_params": {
                    "line": Rad,
                    "dust": Rad
                }
            }
        """

        self.vat = vat_params["Vat"]()
        self.vat.file("Line", vat_params["Line"])

        self.vow = vow_params["Vow"](self.vat, None, None)
        for what in ("wait", "bump", "sump", "dump", "hump"):
            self.vow.file(what, vow_params[what])

        self.cat = cat_params["Cat"](self.vat)
        self.cat.file("vow", self.vow)
        self.cat.file("box", cat_params["box"])

        self.spotter = spotter_params["Spotter"](self.vat)
        self.spotter.file("par", spotter_params["par"])

        self.dai_join = dai_join_params["DaiJoin"](self.vat, dai_join_params["dai"])

        # TODO: Flipper, Flapper, Flopper

        for ilk in ilks:
            for what in ("line", "dust"):
                self.vat.file_ilk(ilk["ilk_id"], what, ilk["vat_params"][what])
            for what in ("chop", "dunk", "flip"):
                self.cat.file_ilk(ilk["ilk_id"], what, ilk["cat_params"][what])
            for what in ("pip", "mat"):
                self.spotter.file_ilk(ilk["ilk_id"], what, ilk["spotter_params"][what])

            self.gem_joins[ilk["ilk_id"]] = gem_join_params["GemJoin"](
                self.vat, ilk["ilk_id"], ilk["gem_join_params"]["gem"]
            )
        self.dispatchers = dispatchers
        self.loggers = loggers
        self.action_sort_key = action_sort_key

    def run(self):
        pass
