""" Token Module
    Class-based representation of ERC-20 tokens
    (contains only what is necessary for the simulation)
"""

from dai_cadcad.util import require


class Token:
    name = ""
    symbol = ""

    totalSupply = 0

    balances = {}

    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

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
            self.balances[from_address] >= value,
            f"{self.symbol}/insufficient-transferFrom",
        )
        self.balances[from_address] -= value
        self.balances[to_address] = self.balances.get(to_address, 0) + value
        return True

    def balanceOf(self, owner):
        return self.balances.get(owner, 0)


Ether = Token("Ether", "ETH")
Dai = Token("Dai", "DAI")
Maker = Token("Maker", "MKR")
