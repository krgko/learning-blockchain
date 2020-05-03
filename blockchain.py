from functools import reduce
from utils.hashutil import hash_block
import hashlib as hl
import json
import pickle

# Treat all as Block object
from block import Block

from transaction import Transaction
from utils.verification import Verification

# Ensure that order correct
from collections import OrderedDict
from wallet import Wallet

MINING_REWARD = 10


class Blockchain:
    def __init__(self, node_id):
        self.genesis_block = Block(0, '', [], 0)
        # Initialized blockchain list
        self.chain = [self.genesis_block]
        self.__open_transactions = []
        self.load_data()
        self.node_id = node_id

    # # global scope variable - can call by anywhere
    # MINING_REWARD = 10

    # # genesis_block = {
    # #     'previous_hash': '',
    # #     'index': 0,
    # #     'transactions': [],
    # #     'proof': 99  # any number, will not use this for calculate hash
    # # }
    # genesis_block = Block(0, '', [], 0)
    # blockchain = [genesis_block]
    # open_transactions = []

    # owner = 'Golf'  # person who send coin to others
    # participants = {'Golf'}

    @property
    def chain(self):
        # return copy of chain and append to chain not the real chain
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        # global blockchain  # Tell python that we have these global vars
        # global open_transactions

        try:
            with open('blockchain.txt', 'r') as f:
                # with open('blockchain.b', 'rb') as f:
                file_content = f.readlines()
                # file_content_b = f.read()
                # if len(file_content_b) != 0:
                # file_content = pickle.loads(file_content_b)
                if len(file_content) != 0:

                    # Failed due to these 2 vars need list not string
                    # loads will retrieve json object from file

                    # OrderedDict will lost if load like this
                    blockchain = json.loads(file_content[0][:-1])
                    updated_blockchain = []
                    # Make data like before store
                    for block in blockchain:
                        converted_txs = [Transaction(
                            tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
                        updated_block = Block(
                            block['index'], block['previous_hash'], converted_txs, block['proof'], block['timestamp'])
                        updated_blockchain.append(updated_block)
                    self.chain = updated_blockchain
                    open_transactions = json.loads(file_content[1])
                    updated_transactions = []
                    for tx in open_transactions:
                        updated_transaction = Transaction(
                            tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                        updated_transactions.append(updated_transaction)
                    self.__open_transactions = updated_transactions
                    # blockchain = file_content['chain']
                    # open_transactions = file_content['ot']
        except (IOError, IndexError):
            # IndexError will handle if blockchain.txt empty
            # When IOError it still support to create block
            # These things will be initialized on constructor automatically
            # genesis_block = Block(0, '', [], 0)
            # blockchain = [genesis_block]
            # open_transactions = []
            pass
        finally:
            print('Start program succeed !!')

    # When changed to the class it will not declared here
    # load_data()

    def save_data(self):
        try:
            with open('blockchain.txt', 'w') as f:
                # Convert object to dict for saving
                saveable_block = [block.__dict__ for block in [
                    Block(b.index, b.previous_hash, [tx.__dict__ for tx in b.transactions], b.proof, b.timestamp) for b in self.__chain]]
                # Can be do like this or apply every transaction
                saveable_transactions = [
                    tx.__dict__ for tx in self.__open_transactions]

                # with open('blockchain.b', 'wb') as f:
                # All blockchain means historical data
                # Cannot use string because can store but cannot use
                # f.write(str(blockchain))
                # f.write('\n')
                # f.write(str(open_transactions))
                # dumps will convert object to string
                f.write(json.dumps(saveable_block))
                f.write('\n')
                f.write(json.dumps(saveable_transactions))
                # Binary data using pickle - cannot do like before because we will not store text
                # save_data = {
                #     'chain': blockchain,
                #     'ot': open_transactions
                # }
                # f.write(pickle.dumps(save_data))
        except IOError:
            print('Saving chain failed')

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        # nonce will step per 1
        proof = 0
        verifier = Verification()
        while not verifier.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self, participant):
        tx_sender = [[tx.amount for tx in block.transactions
                      if tx.sender == participant] for block in self.__chain]
        open_tx_sender = [tx.amount
                          for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = reduce(
            lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
        # amount_sent = 0
        # for tx in tx_sender:
        #     if len(tx) > 0:
        #         amount_sent += tx[0]
        tx_recipient = [[tx.amount for tx in block.transactions
                         if tx.recipient == participant] for block in self.__chain]
        amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(
            tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
        # amount_received = 0
        # for tx in tx_recipient:
        #     if len(tx) > 0:
        #         amount_received += tx[0]
        return amount_received - amount_sent

    def get_last_blockchain_value(self):
        """ Returns the last result of the current blockchain. """

        if len(self.__chain) < 1:
            return None

        # local variable - can call only function scope
        # if global variable has been assign new variable inside function
        # it will not update global variable value because inside function
        # new local variable will be created for function scope
        last_blockchain_value = self.__chain[-1]

        # if need to use global variable it need some keyword is
        # global {variable}
        # {variable} = new_value

        # if index is -1 it will be last element
        return last_blockchain_value

    # add default variable like javascript

    def add_transaction(self, recipient, sender, signature, amount=1.0):
        """ Append a new value to the blockchain

        Arguments:
            :sender: The sender of coins
            :recipient: The recipient of coins
            :amount: The amount of coins (default=1.0)
        """

        # Not allow if None
        if self.node_id == None:
            return False

        # transaction = {
        #     'sender': sender,
        #     'recipient': recipient,
        #     'amount': amount
        # }
        # to prevent order of dict changed
        # transaction = OrderedDict(
        #     [('sender', sender), ('recipient', recipient), ('amount', amount)])
        transaction = Transaction(
            sender, recipient, signature, amount)
        if not Wallet.verify_transaction(transaction):
            return False
            # get_balance will be reference
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            # participants.add(sender)
            # participants.add(recipient)
            self.save_data()
            return True
        return False

    def mine_block(self):
        """ Mine block will append block to blockchain
        """

        # Not allow if None
        if self.node_id == None:
            return False

        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        # proof before add reward transaction
        proof = self.proof_of_work()
        # reward_transaction = {
        #     'sender': 'MINING',
        #     'recipient': owner,
        #     'amount': MINING_REWARD
        # }
        # reward_transaction = OrderedDict(
        #     [('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])
        reward_transaction = Transaction(
            'MINING', self.node_id, '', MINING_REWARD)

        # we don't modify master data so, we need to copy it
        copied_transactions = self.__open_transactions[:]
        copied_transactions.append(reward_transaction)
        # block = {
        #     'previous_hash': hashed_block,
        #     'index': len(blockchain),
        #     'transactions': copied_transactions,
        #     'proof': proof
        # }
        block = Block(len(self.__chain), hashed_block,
                      copied_transactions, proof)
        for tx in block.transactions:
            if not Wallet.verify_transaction(tx):
                return False
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return True

    # duplicate code must to stay as function
