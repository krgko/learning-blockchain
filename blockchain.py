# global scope variable - can call by anywhere
blockchain = []


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
def add_transaction(transaction_amount, last_transaction=[0]):
    """ Append a new value to the blockchain

    Arguments:
        :transaction_amount: The amount that will added into transaction
        :last_transaction: The last blockchain transaction (default [0])
    """
    if last_transaction == None:
        last_transaction = [0]

    blockchain.append([last_transaction, transaction_amount])


# duplicate code must to stay as function
def get_transaction_value():
    """ Returns the input of the user (new transaction amount) as a float """
    return float(input('input amount: '))


def get_user_choice():
    """ Return the user's choice """
    choice = input('choice: ')
    return choice


def print_instructions():
    """ Print instructions for user """
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Output the blockchain blocks')
    print('h: Manipulate the chain')
    print('q: Quit')


def print_blocks():
    """ Print blocks in blockchain """
    print('full chain: ', blockchain)
    # outout of blockchain
    for block in blockchain:
        print('output block: ', block)

def verify_chain():
    block_index = 0
    is_valid = True
    for block in blockchain:
        if block_index == 0:
            block_index += 1
            continue
        # for test only when use 'h' option
        elif block[0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break
        block_index += 1
    return is_valid

# add many block we want
while True:
    print_instructions()
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_amount = get_transaction_value()
        add_transaction(tx_amount, get_last_blockchain_value())
    elif user_choice == '2':
        print_blocks()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == 'q':
        break
    else:
        print('Please input a valid input from choice')
    
    if not verify_chain():
        print('Invalid chain!')
        break

print('Finished')
