from time import time
from printable import Printable


class Block(Printable):
    def __init__(self, index, previous_hash, transactions, proof, time=time()):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.proof = proof
        self.timestamp = time

    def __repr__(self):
        # return 'index: {}, previous_hash: {}, transactions: {}, proof: {}, timestamp: {}'.format(self.index, self.previous_hash, self.transactions, self.proof, self.timestamp)
        return str(self.__dict__)
