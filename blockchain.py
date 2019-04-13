# global scope variable - can call by anywhere
blockchain = []


def get_last_blockchain_value():
    """ Returns the last result of the current blockchain. """

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
def add_value(transaction_amount, last_transaction=[0]):
    """ Append a new value to the blockchain

    Arguments:
        :transaction_amount: The amount that will added into transaction
        :last_transaction: The last blockchain transaction (default [0])
    """
    blockchain.append([last_transaction, transaction_amount])


# duplicate code must to stay as function
def get_user_input():
    """ Returns the input of the user (new transaction amount) as a float """
    return float(input('input amount: '))


tx_amount = get_user_input()
add_value(tx_amount)

tx_amount = get_user_input()
# we can assign value to the correct like this
add_value(last_transaction=get_last_blockchain_value(),
          transaction_amount=tx_amount)

tx_amount = get_user_input()
add_value(tx_amount, get_last_blockchain_value())
print(blockchain)
