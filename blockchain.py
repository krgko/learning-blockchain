from functools import reduce
from utils.hashutil import hash_block
import hashlib as hl
import json
import pickle
import requests

# Treat all as Block object
from block import Block

from transaction import Transaction
from utils.verification import Verification

# Ensure that order correct
from collections import OrderedDict
from wallet import Wallet

# TODO: Mining reward and Difficulty should be stored at blockchain
MINING_REWARD = 10


class Blockchain:
    def __init__(self, public_key, node_id):
        self.genesis_block = Block(0, '', [], 0, 0)
        # Initialized blockchain list
        self.chain = [self.genesis_block]
        self.__open_transactions = []
        self.public_key = public_key
        # For manage nodes
        self.__peer_nodes = set()
        self.node_id = node_id
        # No need to resolve conflicts
        self.resolve_conflicts = False
        # Load after declare variable
        self.load_data()

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
            with open(f'blockchain-{self.node_id}.txt', 'r') as f:
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
                    # new line can enable to load data as array
                    peer_nodes = json.loads(file_content[2])
                    self.__peer_nodes = set(peer_nodes)
        except (IOError, IndexError):
            # IndexError will handle if blockchain.txt empty
            # When IOError it still support to create block
            # These things will be initialized on constructor automatically
            # genesis_block = Block(0, '', [], 0)
            # blockchain = [genesis_block]
            # open_transactions = []
            pass
        finally:
            pass

    # When changed to the class it will not declared here
    # load_data()

    def save_data(self):
        try:
            with open(f'blockchain-{self.node_id}.txt', 'w') as f:
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
                f.write("\n")
                f.write(json.dumps(list(self.__peer_nodes)))
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

    def get_balance(self, sender=None):
        if sender == None:
            if self.public_key == None:
                return None
            participant = self.public_key
        else:
            participant = sender
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

    def add_transaction(self, recipient, sender, signature, amount=1.0, is_receiving=False):
        """ Append a new value to the blockchain

        Arguments:
            :sender: The sender of coins
            :recipient: The recipient of coins
            :signature: The signature of transaction
            :amount: The amount of coins (default=1.0)
            :is_receiving: For reusing of method
        """

        # Not allow if None
        if self.public_key == None:
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
        # Do in Verification.verify_transaction
        # if not Wallet.verify_transaction(transaction):
        #     return False
        # get_balance will be reference

        # Validate it self then sent to other node to validate with
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            # participants.add(sender)
            # participants.add(recipient)
            self.save_data()
            if not is_receiving:
                # If does not do this it will broadcast forever
                for node in list(self.__peer_nodes):
                    # TODO: Validation for node name when save
                    url = 'http://{}/broadcast-transaction'.format(node)
                    # Send an exists data to other nodes
                    try:
                        response = requests.post(url, json={
                            'sender': sender,
                            'recipient': recipient,
                            'amount': amount,
                            'signature': signature,
                        })
                        if response.status_code == 400 or response.status_code == 500:
                            print('Transaction declined, need resolving')
                            return False
                    except requests.exceptions.ConnectionError:
                        print('Cannot connect to peer node')
                        continue
            return True
        return False

    def add_block(self, block):
        transactions = [Transaction(
            tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
        proof_is_valid = Verification.valid_proof(
            transactions[:-1], block['previous_hash'], block['proof'])
        hashes_match = hash_block(self.chain[-1]) == block['previous_hash']
        if not proof_is_valid or not hashes_match:
            return False
        # FIXME: Due to this solution the block timestamp should be UTC only for preventing time diff
        converted_block = Block(
            block['index'], block['previous_hash'], transactions, block['proof'], block['timestamp'])
        self.__chain.append(converted_block)
        # Update open transactions on peer node when add_block
        stored_transactions = self.__open_transactions[:]
        for incoming_tx in block['transactions']:
            for opentx in stored_transactions:
                if opentx.sender == incoming_tx['sender'] and opentx.recipient == incoming_tx['recipient']:
                    try:
                        # Remove with an exact match key
                        self.__open_transactions.remove(opentx)
                    except ValueError:
                        print('Open transaction was removed')
        # self.__open_transactions = [] # Might be another way
        self.save_data()
        return True

    def mine_block(self):
        """ Mine block will append block to blockchain
        """

        # Not allow if None
        if self.public_key == None:
            return None

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
            'MINING', self.public_key, '', MINING_REWARD)

        # we don't modify master data so, we need to copy it
        copied_transactions = self.__open_transactions[:]
        # Check before append to the block the new transaction
        # That's why verify copied_transactions exclude MINING block
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return None
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block,
                      copied_transactions, proof)
        # block = {
        #     'previous_hash': hashed_block,
        #     'index': len(blockchain),
        #     'transactions': copied_transactions,
        #     'proof': proof
        # }
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        for node in self.__peer_nodes:
            url = 'http://{}/broadcast-block'.format(node)
            converted_block = block.__dict__.copy()
            # Convert them to dict format
            converted_block['transactions'] = [tx.__dict__
                                               for tx in converted_block['transactions']]
            try:
                response = requests.post(url, json={
                    'block': converted_block
                })
                if response.status_code == 400 or response.status_code == 500:
                    print('Block declined, need resolving')
                if response.status_code == 409:
                    self.resolve_conflicts = True
            except requests.exceptions.ConnectionError:
                print('Cannot connect to peer node')
                continue
        return block

    def resolve(self):
        """Sync the blockchain with other node when it does not conflict
        """
        # FIXME: Should be compare with all node within the network and trust the majority nodes, also automatically download peer_nodes | Better to do this when start node
        main_chain = self.chain
        replace = False
        # Dump data from any block
        for node in self.__peer_nodes:
            url = 'http://{}/chain'.format(node)
            try:
                response = requests.get(url)
                node_chain = response.json()  # Return a list
                node_chain = [Block(block['index'], block['previous_hash'],
                                    [Transaction(
                                        tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']], block['proof'], block['timestamp']) for block in node_chain]
                node_chain_length = len(node_chain)
                local_chain_length = len(self.chain)
                # If longer means local chain is invalid, else use current chain
                if node_chain_length > local_chain_length and Verification.verify_chain(node_chain):
                    main_chain = node_chain
                    replace = True  # Indicate the chain does not valid so transaction will not appended to block and block will not appended to chain
            except requests.exceptions.ConnectionError:
                continue
        self.resolve_conflicts = False
        self.chain = main_chain
        if replace:
            # Reset the open transaction which is append to block of invalid chain
            self.__open_transactions = []
        self.save_data()
        return replace

    # duplicate code must to stay as function
    def add_peer_node(self, node):
        """Add a new node to the peer node set

        Arguments:
            :node: The node URL to add
        """
        # Set methods: https://www.w3schools.com/python/python_ref_set.asp
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        """Remove a new node to the peer node set

        Arguments:
            :node: The node URL to remove
        """
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_peer_nodes(self):
        """Return a list of all connected peer nodes"""
        return list(self.__peer_nodes)
