""" Prices Module

Contains functions for generating price feeds using CoinAPI.

Current approach is to sample from historical data, rather than fully simulating price feeds, or
just using historical data out-the-box.
"""

from coinapi_rest_v1 import coinapi_rest_v1

from dai_cadcad import environment

coin_api = coinapi_rest_v1.CoinAPIv1(environment.COIN_API_KEY)


def get_historic_price_feed(symbol_id, time_range):
    """ Fetches historic a price feed (in USD) for the given coin (ETH, DAI, MKR) and time range.

        `symbol_id` is a string representing an asset trading pair on a given exchange, which can
        be found in /coinapi_symbols.json.

        `time_range` is a 2-value array with ISO 8601 "from" and "to" timestamps, respectively.

        TODO: Currently too lazy to implement checking against `time_range` to see if multiple
        API calls are necessary, should the limit of 100000 data points be exceeded. As of now this
        allows us a time range of <= 69 days (lol).
    """

    ohlcv_historical = coin_api.ohlcv_historical_data(
        symbol_id,
        {
            "period_id": "1MIN",
            "time_start": time_range[0],
            "time_end": time_range[1],
            "limit": 100000,
        },
    )

    return [period["price_close"] for period in ohlcv_historical]
