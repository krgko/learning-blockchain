from verification import Verification

class Node:
    def __init__(self, add_transaction, open_transactions):
        self.blockchain = []
        self.add_transaction = add_transaction
        self.open_transactions = open_transactions

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

    def print_blocks(self, blockchain):
        """ Print blocks in blockchain """
        print('full chain: ', blockchain)
        # outout of blockchain
        for block in blockchain:
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
                if add_transaction(recipient=recipient, amount=amount):
                    print('Added transaction')
                else:
                    print('Transaction failed')
                print(open_transactions)
            elif user_choice == '2':
                if mine_block():
                    open_transactions = []
                    save_data()
            elif user_choice == '3':
                self.print_blocks(self.blockchain)
            elif user_choice == '4':
                verifier = Verification()
                if verifier.verify_transactions(open_transactions, get_balance):
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
            if not verifier.verify_chain(self.blockchain):
                self.print_blocks(self.blockchain)
                print('Invalid chain!')
                break

            print('Balance of {} is {:.10}'.format(
                owner, str(get_balance(owner))))
        else:
            print('User left!')
