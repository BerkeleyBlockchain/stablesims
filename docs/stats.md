# Stats

## Overview
<!-- TODO: move module definitions here? -->
A set of methods used to calculate statistics over the course of an
experiment.
Each such method is a higher-order function returning a `track_stat` method
that takes in an Experiment object, an action key, and the address of the
Keeper that executed said action.
The higher-order function can take in whatever parameters it may need to
provide to `track_stat`.
Each `track_stat` function will be run after a Keeper executes in an action
in a timestep, so an intended design pattern is to guard your logic in
`track_stat` w/ a predicate that ensures you're only executing the method
in response to a specific action you were listening for.

## Common Conventions

## Functions
### ilk_price

Updates the ilk values in `stats`.

### num_new_bites

Updates the number of new bites in `stats`

### num_bids_places

Updates the number of bids placed in `stats`

### num_active_bids

Updates the number of current active bids across all ilks and flippers in `stats`.

### keeper_gem_balances

Updates the balances of ilk for each keeper in `stats`.
