# global scope variable - can call by anywhere
genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Golf'  # person who send coin to others
participants = {'Golf'}


def hash_block(block):
    return ''.join([str(block[key]) for key in block])


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

    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    open_transactions.append(transaction)
    participants.add(sender)
    participants.add(recipient)


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)

    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': open_transactions
    }
    blockchain.append(block)

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
    return True


waiting_for_input = True

# add many block we want
while waiting_for_input:
    print_instructions()
    user_choice = get_user_choice()
    if user_choice == '1':
        # like destructure of javascript
        recipient, amount = get_transaction_value()
        # add the transaction to blockchain
        add_transaction(recipient=recipient, amount=amount)
        print(open_transactions)
    elif user_choice == '2':
        mine_block()
    elif user_choice == '3':
        print_blocks()
    elif user_choice == '4':
        print(participants)
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
else:
    print('User left!')

print('Finished')
