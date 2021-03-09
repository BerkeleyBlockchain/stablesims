# Smart Contracts

## Overview

We've only ported over the smart contracts necessary for our simulations. This currently includes:
| Our implementation | Maker implementation |
| - | - |
| [`cat.py`](../pydss/cat.py) | [`cat.sol`](https://github.com/makerdao/dss/blob/master/src/cat.sol) |
| [`flip.py`](../pydss/flip.py) | [`flip.sol`](https://github.com/makerdao/dss/blob/master/src/flip.sol) |
| [`join.py`](../pydss/join.py) | [`join.sol`](https://github.com/makerdao/dss/blob/master/src/join.sol) |
| [`spotter.py`](../pydss/spotter.py) | [`spot.sol`](https://github.com/makerdao/dss/blob/master/src/spot.sol) |
| [`vat.py`](../pydss/vat.py) | [`vat.sol`](https://github.com/makerdao/dss/blob/master/src/vat.sol) |
| [`vow.py`](../pydss/vow.py) | [`vow.sol`](https://github.com/makerdao/dss/blob/master/src/vow.sol) |

In addition to these smart contracts from the Dai stablecoin system (DSS), we've also created a `Token` class that loosely mimics the [ERC-20 spec](https://eips.ethereum.org/EIPS/eip-20) / [dai.sol](https://github.com/makerdao/dss/blob/master/src/dai.sol) contract.

Finally, to handle the protocol's fixed-point integer `Wad`, `Rad`, and `Ray` units, we simply forked the `numeric.py` package from Maker's [`pymaker`](https://github.com/makerdao/pymaker) package.

## Common Conventions

The guiding principle in implementing these smart contract classes was to **replicate the Maker source code as closely as possible.** This even included variable naming conventions, with some slight adjustments.

### `self.ADDRESS`

This is the only field shared by all smart contract classes (it's purpose should be evident).
There's no smart contract base class, nor other shared abstractions (e.g. `msg.sender` functionality) - that's pushing into territory we deemed to be low-level for StableSims.

### `Ilk` / `Bid` class redefinition

In files such as `vat.py` and `cat.py`, there are different definitions of the `Ilk` class. While their contents are slightly different, one might stop to ponder why we didn't consolidate all of the fields into one top-level `Ilk` class, or set up an inheritance structure of any sort.

The reason for this, is that such is the layout of the Maker source code. The `Ilk` struct is redefined as best fit in the smart contracts where it's used.

You'll see redefinitions of the `Bid` class in the `Flipper`, `Flapper`, and `Flopper` smart contracts (WIP) as well, according to the same convention.

### Extra parameters

In some cases, you might spot additional method parameters that aren't present in the Maker source code, namely `now` and `sender`. These correspond to the expressions `now` and `msg.sender` in Solidity, respectively. They are only passed in when needed in the method.

Should we ever make a base smart contract class, this time- and caller-awareness functionality should be encapsulated by it.

### Missing & extra logic

Occasionally, you may find logical discrepancies between our code and the Maker source code. For example, we are missing some smart contract functions, such as `hope` and `nope` on the `Vat`, and omit these function calls wherever they should appear in the code. Logic is only ommitted when it isn't necessary for our simulations.

Sometimes, on the other hand, you'll see tidbits of extraneous logic - likely a bunch of instance variable-setting in a smart contract class's `__init__` method. This is necessary to match the default instantiation of variables in Solidity.

### Variable naming

As mentioned, variable names were copied from the source code in almost all cases. However, for consistency in variable naming outside of the smart contract classes, the following exceptions are made:
1. Wherever the variable name `ilk` was used in the source code to refer to the address of an Ilk, we use the variable name `ilk_id`
   - Note that this doesn't include e.g. the `frob` method of the `Vat` contract, where the Ilk's address is denoted by the parameter `i`.
2. Wherever the variable name `bid` was used in the source code to refer to the address of a Bid, we use the variable name `bid_id`
3. The Ilk-specific `file` methods (e.g. those in `Cat` and `Vat` that take an `ilk_id` parameter) are renamed to `file_ilk` to avoid method overloading.
