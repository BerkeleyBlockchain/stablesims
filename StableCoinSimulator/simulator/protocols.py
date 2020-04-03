from collections import deque
import time
from .constants import *

class BasisBond: 
    def __init__(self, tid, timestamp, amount, expiry):
        self.tid = tid
        self.timestamp = int(timestamp)
        self.expirytime = self.timestamp + expiry
        self.amount = amount

class Protocol:
    def __init__(self, totalSupply):
        self.totalSupply = totalSupply
        self.market = None
        
    def update(self):
        pass
        
class BasisProtocol(Protocol):
    
    def __init__(self, totalSupply, market):
        super().__init__(totalSupply)
        self.market = market
        self.bond_expiry = BOND_EXPIRY # 5 year expiry
        self.bondsForAuction = 0
        self.bondQueue = deque()
        self.bondQueueLength = 0
        self.delay = BOND_DELAY # In Steps
        self.lastAuction = 0 # Last aucion
        self.currentStep = 0
        
    def issueBonds(self, tid, amount):
        self.bondQueue.append(BasisBond(tid, time.time(), amount, self.bond_expiry))
        self.bondsForAuction -= amount
        self.bondQueueLength += amount
        
        # Basis are burnt outside of this code 
        
    def update(self):
        price = self.market.getCurrentUSDValue()
        self.currentStep += 1
        
        LOWER, UPPER = BOND_RANGE
        
        if self.currentStep < self.lastAuction + self.delay:
            return

        # ISSUE bonds
        if price < LOWER:
            bondsToCreate = (1. - price) * self.market.getCirculation() 
            self.bondsForAuction += bondsToCreate
            self.lastAuction = self.currentStep
            
        elif price > UPPER:
            basisToCreate = (price - 1.) * self.market.getCirculation() 
            self.lastAuction = self.currentStep
            
            while len(self.bondQueue) and basisToCreate:
                head = self.bondQueue.popleft()
                if head.amount > basisToCreate:
                    self.market.traderPool[head.tid].liquidate(head.amount)
                    head.amount -= basisToCreate
                    basisToCreate = 0
                    self.bondQueue.appendleft(head)
                    self.bondQueueLength -= basisToCreate
                else:
                    self.market.traderPool[head.tid].liquidate(head.amount)
                    basisToCreate -= head.amount
                    self.bondQueueLength -= head.amount
                    
            if basisToCreate > 0:
                # Distribute to shareholders
                pass
            