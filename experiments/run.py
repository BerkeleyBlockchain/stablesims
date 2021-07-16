""" Run Simultions
sim="[SIM_NAME]" python3 run.py
"""

import os
import sys
from experiments.dutch_auctions.dutch_auctions_bull_sim import DutchAuctionsBull
from experiments.dutch_auctions.dutch_auctions_bear_sim import DutchAuctionsBear

def run(sim):
  if (sim == 'DutchAuctionsBull'):
    DutchAuctionsBull.run()
  elif (sim == 'DutchAuctionsBear'):
    DutchAuctionsBear.run()

if __name__ == "__main__":
    sim = os.getenv("sim")

    if not (sim):
        print("Please enter simulation name ")
        sys.exit()

    