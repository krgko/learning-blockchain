from uuid import uuid4
from blockchain import Blockchain
from verification import Verification


class Node:
    def __init__(self):
        self.id = str(uuid4())
        self.blockchain = Blockchain(self.id)

    def get_transaction_value(self):
        """ Returns the input of the user (new transaction amount) as a float """
        tx_recipient = input('Recipient of transaction: ')
        tx_amount = float(input('Input amount: '))
        return tx_recipient, tx_amount

    def get_user_choice(self):
        """ Return the user's choice """
        choice = input('Choice: ')
        return choice

    def print_instructions(self):
        """ Print instructions for user """
        print('Please choose')
        print('1: Add a new transaction value')
        print('2: Mine a new block')
        print('3: Output the blockchain blocks')
        print('4: Check transaction validlity')
        # print('h: Manipulate the chain')
        print('q: Quit')

    def print_blocks(self):
        """ Print blocks in blockchain """
        # print('full chain: ', self.blockchain.chain)
        # outout of blockchain
        for block in self.blockchain.chain:
            print('output block: ', block)
        else:
            print('-' * 20)

    def listen_for_input(self):
        waiting_for_input = True

        # add many block we want
        while waiting_for_input:
            self.print_instructions()
            user_choice = self.get_user_choice()
            if user_choice == '1':
                # like destructure of javascript
                recipient, amount = self.get_transaction_value()
                # add the transaction to blockchain
                if self.blockchain.add_transaction(recipient=recipient, sender=self.id, amount=amount):
                    print('Added transaction')
                else:
                    print('Transaction failed')
                print(self.blockchain.open_transactions)
            elif user_choice == '2':
                self.blockchain.mine_block()
                # Do it on blockchain class is make more sense
                # open_transactions = []
                # self.blockchain.save_data()
            elif user_choice == '3':
                self.print_blocks()
            elif user_choice == '4':
                verifier = Verification()
                if verifier.verify_transactions(self.blockchain.open_transactions, self.blockchain.get_balance):
                    print('All transactions valid')
                else:
                    print('There is invalid transaction!')
            # elif user_choice == 'h':
            #     if len(blockchain) >= 1:
            #         blockchain[0] = {
            #             'previous_hash': '',
            #             'index': 0,
            #             'transactions': [{'sender': owner, 'recipient': 'Hacker', 'amount': 100000}]
            #         }
            elif user_choice == 'q':
                # change the value to break the loop
                waiting_for_input = False
            else:
                print('Please input a valid input from choice')
            verifier = Verification()
            if not verifier.verify_chain(self.blockchain.chain):
                self.print_blocks()
                print('Invalid chain!')
                break

            print('Balance of {} is {:.10}'.format(
                self.id, str(self.blockchain.get_balance(self.id))))
        else:
            print('User left!')
        print('Finished')


node = Node()
node.listen_for_input()
