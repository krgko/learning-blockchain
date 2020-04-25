from hashutil import hash_block, hs256

DIFFICULTY = 2


class Verification:
    @classmethod
    def valid_proof(cls, transactions, last_hash, proof):
        # make puzzle question
        # guess = (str(transactions) + str(last_hash) + str(proof)).encode()
        guess = (str([tx.to_ordered_dict() for tx in transactions]) +
                 str(last_hash) + str(proof)).encode()
        guess_hash = hs256(guess)
        # print(guess_hash)
        # why guess_hash will not change when do other things except mine
        # because guess hash calculated will be the same when transaction not added

        # checking valid hash 00 - 00 is difficulty
        return guess_hash[0: DIFFICULTY] == '0' * DIFFICULTY

    @classmethod
    def verify_chain(cls, blockchain):
        """ Verify the blockchain if return True that means the blockchain is valid """
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue  # genesis block hash no one maniplate
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            # check valid_proof before add reward
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                return False
        return True

    @staticmethod
    def verify_transaction(transaction, get_balance):
        sender_balance = get_balance(transaction.sender)
        return sender_balance >= transaction.amount

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        """ Verify transaction list """
        return all([cls.verify_transaction(tx, get_balance) for tx in open_transactions])
