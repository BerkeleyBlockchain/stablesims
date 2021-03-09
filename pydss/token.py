""" Token Module
    Class-based representation of ERC-20 tokens
    (contains only what is necessary for the simulation)
"""

from pydss.util import require


class Token:
    """
    symbol = str
    totalSupply = int
    balances = dict[str: float]
    """

    def __init__(self, symbol):
        self.symbol = symbol
        self.totalSupply = 0
        self.balances = {}

    def mint(self, owner, value):
        self.balances[owner] = self.balances.get(owner, 0) + value
        self.totalSupply += value
        return True

    def burn(self, owner, value):
        require(self.balances[owner] >= value, f"{self.symbol}/insufficient-burn")
        self.balances[owner] -= value
        self.totalSupply -= value
        return True

    def transferFrom(self, from_address, to_address, value):
        require(
            not from_address or self.balances[from_address] >= value,
            f"{self.symbol}/insufficient-transferFrom",
        )
        if from_address:
            self.balances[from_address] -= value
        self.balances[to_address] = self.balances.get(to_address, 0) + value
        return True

    def balanceOf(self, owner):
        return self.balances.get(owner, 0)


Ether = Token("ETH")
Dai = Token("DAI")
Maker = Token("MKR")
