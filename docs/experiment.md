# Experiment

## Overview
### action
Actions are the atomic signals passed between the simulation engine and simulation agents (keepers).
- `key` states the type of action (currently `OPEN_VAULT`, `DENT`, `TEND`, `DEAL`, `POKE`, `BITE`).
- `keeper` states the keeper that is performing the action.
- `handler` states the function that will be called.
- `args` states the arguments that will be passed to the `handler`.
- `kwargs` states any additional arguments that are needed.

## Common Conventions

## Functions

### init
- contracts: dict of smart contract classes, e.g. {"Cat": MyCustomCatClass}
- keepers: dict of keeper classes, e.g. {"MyCustomKeeper": MyCustomKeeperClass}
- sort_actions: sort key used to decide the order in which keepers act each timestep
- ilk_ids: list of ilks by their ticker symbol
- Token: token class
- stat_trackers: list of methods that measure stats over the course of the experiment, e.g.: [num_new_kicks]
- parameters: dict of parameters used to instantiate the contracts, keepers, and simulation, e.g.: {"Spotter": {...}, "MyCustomKeeper": {...}, "timesteps": ...
### run
The core function of the simulation.
Initializes assets, smart contracts, state, and keepers.
One timestep consists of the following:
- send an `action` object to signal stat-tracking functions to begin tracking data.
- iterates through
- send an `action` object to signal stat-tracking functions to end tracking data.