from uuid import uuid4
from blockchain import Blockchain
from utils.verification import Verification
from wallet import Wallet


class Node:
    def __init__(self):
        self.wallet = Wallet()
        # self.id = str(uuid4())
        self.blockchain = None

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
        if self.wallet.public_key != None:
            print('1: Add a new transaction value')
            print('2: Mine a new block')
            print('3: Output the blockchain blocks')
            print('3f: Output the blockchain blocks - full block')
            print('4: Check transaction validlity')
        print('5: Create wallet')  # create priv and pub
        print('6: Load wallet')
        print('7: Save wallet')
        # print('h: Manipulate the chain')
        print('q: Quit')

    def print_blocks(self, simplified=False):
        """ Print blocks in blockchain """
        # print('full chain: ', self.blockchain.chain)
        # outout of blockchain
        simplified = bool(simplified)
        if simplified:
            # Access the copy of the chain
            for (index, block) in enumerate(self.blockchain.chain):
                simplify_block = [
                    transaction.amount for transaction in block.transactions if transaction.sender != "MINING"]
                print(f"block {str(index)}: {simplify_block}")
            return

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
            if (self.wallet.public_key == None) and (user_choice in ['1', '2', '3', '4', '3f']):
                print("Please create wallet or load wallet before do anythings")
                continue

            if user_choice == '1':
                # like destructure of javascript
                recipient, amount = self.get_transaction_value()
                # add the transaction to blockchain
                signature = self.wallet.sign_transaction(
                    self.wallet.public_key, recipient, amount)
                if self.blockchain.add_transaction(recipient=recipient, sender=self.wallet.public_key, signature=signature, amount=amount):
                    print('Added transaction')
                else:
                    print('Transaction failed')
                print(self.blockchain.get_open_transactions())
            elif user_choice == '2':
                if not self.blockchain.mine_block():
                    print("Minine failed. No wallet attached")
                # Do it on blockchain class is make more sense
                # open_transactions = []
                # self.blockchain.save_data()
            elif user_choice == '3':
                self.print_blocks(simplified=True)
            elif user_choice == '3f':
                self.print_blocks()
            elif user_choice == '4':
                # We can do this due to change to classmethod or statismethod - no need self
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
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
            elif user_choice == '5':
                self.wallet.create_keys()
                # This data will persist per each wallet
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '7':
                self.wallet.save_keys()
            elif user_choice == 'q':
                # change the value to break the loop
                waiting_for_input = False
            else:
                print('Please input a valid input from choice')
            if (user_choice != 'q') and (not Verification.verify_chain(self.blockchain.chain)):
                self.print_blocks()
                print('Invalid chain!')
                break

            if (user_choice not in ['q', '3', '4']) and (self.wallet.public_key != None):
                print('Balance of {} is {:.10}'.format(
                    self.wallet.public_key, str(self.blockchain.get_balance(self.wallet.public_key))))
        else:
            print('User left!')
        print('Finished')


# If need to import somewhere
if __name__ == '__main__':
    node = Node()
    node.listen_for_input()
