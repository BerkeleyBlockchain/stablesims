# Keepers

## Overview

## Common Conventions

The Keeper class follows similar conventions as the smart contracts. See [smart_contracts.md](./smart_contracts.md) for explanations.

## Classes
### Keeper

The base interface for all other keeper classes. `generate_actions_for_timestep` returns an array of `action` objects that is run by [experiment.py](../experiments/experiment.py)

### VaultKeeper

Class representation of a keeper who opens vaults. `open_max_vaults` will open the maximum possible number of vaults for each ilk.

### NaiveVaultKeeper

The Naive Vault Keeper will open the maximum number of vaults possible at each timestep.

### AuctionKeeper

The base interface for auction keeper classes. 
`find_bids_to_place` will take `now` (current timestep as String TODO) as input and will output a dictionary with `ilk_ids` as keys and lists of bids as values.
`run_bidding_model` will take `bid`, `ilk_id` as inputs and will output a dictionary with "price" as a key and the bid price as the value.
`place_bid` will take `bid_id`, `price`,`ilk_id`, `now` as inputs and will output an `action` object.
`find_bids_to_deal` will take `now` as input and will output
`deal_bid` will take `bid_id`, `ilk_id`, `now` as inputs and will output

### FlipperKeeper

The base interface for all other Flipper Keeper classes. The Flipper Keeper will open the maximum number of vaults possible at each timestep. It will also find, deal, and place bids during both dent and tend phases.
`find_and_deal_bids` will add additional deal actions to the `actions` array. 
`deal_bids` converts bid information into an `action` object. Used to claim a winning bid.

### NaiveFlipperKeeper

The Naive Flipper Keeper will start an auction with a bid value that is 5% of the tab/lot. Consecutive bids will increase by the beg + random noise.

### PatientFlipperKeeper

Runs the same bidding model as the Naive Flipper Keeper, however will only place bids when other keepers have 0 DAI balances.

### SpotterKeeper

Will update the `ilk_id` prices.

### BiteKeeper

Will bite urns with liquidation ratios that are too low.
