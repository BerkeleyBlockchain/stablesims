# StableSims

StableSims is an open-source research project aimed at simulating potential defenses against malicious Keeper activity in the [Maker Protocol](https://makerdao.com/en/) during flash crashes such as the "Black Thursday" event of March 12th, 2020.

This project is conducted through [Blockchain @ Berkeley](http://blockchain.berkeley.edu/), utilizes the [cadCAD](https://github.com/cadCAD-org/cadCAD) simulation library, and TAKES NO CREDIT FOR THE MAKER PROTOCOL LOGIC THAT WAS COPIED VERBATIM FROM THE [SOURCE CODE](https://github.com/makerdao/dss).

Check out our [docs](./docs/) for more technical info!

## Simulating the Maker Protocol's "Black Thursday"

### Context: Black Thursday

On March 12th, 2020, the price of ETH crashed from ~$194 to ~$110 in response to widespread uncertainty stemming from the outbreak of the COVID-19 pandemic.

As the markets churned, Ethereum saw an incredibly high rate of transactions (amplified by dummy transactions meant to clog the mempool), spiking gas prices & network congestion.

The drop in ETH price meant that vaults (CDPs) in the Maker Protocol would go undercollateralized, but network congestion meant that Maker's price oracles would delay updating in-system price. Why does this matter?

Keepers knew ahead of time that liquidations would trigger, and had a chance to stock up on DAI for bids in the triggered collateral auctions. The resulting lack of DAI liquidity prevented Keepers from recycling their profits & participating in many auctions.

A couple Keepers started placing near-zero bids on collateral auctions, which went uncontested because other Keepers didn't have the DAI to put up a counter bid, or couldn't get their transactions through the mempool.

An estimated **$8.32M** in ETH was won (essentially stolen from vault owners) by placing these zero-bids.

Sources:
- https://blog.makerdao.com/the-market-collapse-of-march-12-2020-how-it-impacted-makerdao/
- https://www.blocknative.com/blog/mempool-forensics

### Our Response

When we heard about what happened, our first thought, like many others, was, "what could Maker have done differently?" We started toying around with some ideas for defenses, and the more we did so, the more we wanted to test what we had come up with. However, there didn't exist a reasonable way to do this. Working on a local testchain with the Maker Protocol would introduce far too much unnecessary complexity, and would run far too slow for us to get much done.

Thus, the idea for StableSims was born: create an off-chain simulation of the Maker Protocol for rapid experimentation.

### Research

We created StableSims with the intention of testing the following tweaks to the Maker protocol:

1. Dutch auctions (rather than English auctions)
2. Constant ability to trade MKR/DAI with the protocol (as opposed to only during debt/surplus auctions)
3. Automatic vault recollateralization using flash loans (already possible, but not supported at the protocol level)

Once we're done experimenting, we'll be summarizing our findings in a paper. Keep an eye out for it!

