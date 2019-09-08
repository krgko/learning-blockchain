from functools import reduce
from hashutil import hash_block, hs256
import hashlib as hl
import json

# Ensure that order correct
from collections import OrderedDict

# global scope variable - can call by anywhere
MINING_REWARD = 10
DIFFICULTY = 2

genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 99  # any number, will not use this for calculate hash
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Golf'  # person who send coin to others
participants = {'Golf'}


def valid_proof(transactions, last_hash, proof):
    # make puzzle question
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hs256(guess)
    print(guess_hash)
    # why guess_hash will not change when do other things except mine
    # because guess hash calculated will be the same when transaction not added

    # checking valid hash 00 - 00 is difficulty
    return guess_hash[0:DIFFICULTY] == '0' * DIFFICULTY


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    # nonce will step per 1
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount']
                      for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    # amount_sent = 0
    # for tx in tx_sender:
    #     if len(tx) > 0:
    #         amount_sent += tx[0]
    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participant] for block in blockchain]
    amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(
        tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    # amount_received = 0
    # for tx in tx_recipient:
    #     if len(tx) > 0:
    #         amount_received += tx[0]
    return amount_received - amount_sent


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def get_last_blockchain_value():
    """ Returns the last result of the current blockchain. """

    if len(blockchain) < 1:
        return None

    # local variable - can call only function scope
    # if global variable has been assign new variable inside function
    # it will not update global variable value because inside function
    # new local variable will be created for function scope
    last_blockchain_value = blockchain[-1]

    # if need to use global variable it need some keyword is
    # global {variable}
    # {variable} = new_value

    # if index is -1 it will be last element
    return last_blockchain_value


# add default variable like javascript
def add_transaction(recipient, amount=1.0, sender=owner):
    """ Append a new value to the blockchain

    Arguments:
        :sender: The sender of coins
        :recipient: The recipient of coins
        :amount: The amount of coins (default=1.0)
    """

    # transaction = {
    #     'sender': sender,
    #     'recipient': recipient,
    #     'amount': amount
    # }
    # to prevent order of dict changed
    transaction = OrderedDict([('sender', sender), ('recipient', recipient), ('amount', amount)])
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    # proof before add reward transaction
    proof = proof_of_work()
    # reward_transaction = {
    #     'sender': 'MINING',
    #     'recipient': owner,
    #     'amount': MINING_REWARD
    # }
    reward_transaction = OrderedDict([('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])

    # we don't modify master data so, we need to copy it
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof
    }
    blockchain.append(block)
    return True

# duplicate code must to stay as function


def get_transaction_value():
    """ Returns the input of the user (new transaction amount) as a float """
    tx_recipient = input('Recipient of transaction: ')
    tx_amount = float(input('Input amount: '))
    return tx_recipient, tx_amount


def get_user_choice():
    """ Return the user's choice """
    choice = input('Choice: ')
    return choice


def print_instructions():
    """ Print instructions for user """
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('4: Output participants')
    print('5: Check transaction validlity')
    print('h: Manipulate the chain')
    print('q: Quit')


def print_blocks():
    """ Print blocks in blockchain """
    print('full chain: ', blockchain)
    # outout of blockchain
    for block in blockchain:
        print('output block: ', block)
    else:
        print('-' * 20)


def verify_chain():
    """ Verify the blockchain if return True that means the blockchain is valid """
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue  # genesis block hash no one maniplate
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
        # check valid_proof before add reward
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            return False
    return True


def verify_transactions():
    """ Verify transaction list """
    return all([verify_transaction(tx) for tx in open_transactions])


waiting_for_input = True

# add many block we want
while waiting_for_input:
    print_instructions()
    user_choice = get_user_choice()
    if user_choice == '1':
        # like destructure of javascript
        recipient, amount = get_transaction_value()
        # add the transaction to blockchain
        if add_transaction(recipient=recipient, amount=amount):
            print('Added transaction')
        else:
            print('Transaction failed')
        print(open_transactions)
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
    elif user_choice == '3':
        print_blocks()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions valid')
        else:
            print('There is invalid transaction!')
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': owner, 'recipient': 'Hacker', 'amount': 100000}]
            }
    elif user_choice == 'q':
        # change the value to break the loop
        waiting_for_input = False
    else:
        print('Please input a valid input from choice')

    if not verify_chain():
        print_blocks()
        print('Invalid chain!')
        break

    print('Balance of {} is {:.10}'.format(owner, str(get_balance(owner))))
else:
    print('User left!')

print('Finished')
