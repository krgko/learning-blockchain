blockchain = [[0]]


def get_last_blockchain_value():
    # if index is -1 it will be last element
    return blockchain[-1]


def add_value(transaction_ampunt):
    blockchain.append([get_last_blockchain_value(), transaction_ampunt])


add_value(1)
add_value(2)
add_value(3)
print(blockchain)
