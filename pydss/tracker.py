class auction:
    def __init(self, incentive,debt,col_rat):
        self.bid_amt = 0
        self.incentive =incentive
        self.diff_keep = 0
        self.t_keep = 0
        self.restart = 0
        self.slippage = 0
        self.debt = debt

        self.col_rat = col_rat
        self.final = 0;
    def process(self):
        self.net_bid = self.final - self.incentive-self.debt
        self.pct_diff = self.final/self.debt;
        self.liquid = self.final - self.col_rat*self.debt
        self.insolvent = self.final - self.debt