# Stats

## Overview
A set of methods used to calculate statistics over the course of an
experiment.
Each such method is a higher-order function returning a `track_stat` method
that takes in a `state` object from an `Experiment`'s `run` method, and an `action` object.
The higher-order function can take in whatever parameters it may need to
provide to `track_stat`.
Each `track_stat` function will be run after a Keeper executes in an action
in a timestep, so an intended design pattern is to guard your logic in
`track_stat` w/ a predicate that ensures you're only executing the method
in response to a specific action you were listening for.

## Common Conventions
Each `track_stat` function is expected to record its statistic in the `state["stats"]` dict that is part of `experiment.py`. The key will be equivalent to the higher-order function's name (e.g. `num_bids_placed` is the name of the HOF, and also we save the result to `state["stats"]["num_bids_placed"]`.

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
