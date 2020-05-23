from Crypto.PublicKey import RSA
# Algorithm for signature generate RSA sig protocol
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random as rn
import binascii


class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def save_keys(self):
        """Keypair will create from this method only. This will prevent to save new key only"""
        if self.private_key != None and self.private_key != None:
            try:
                with open("wallet.txt", mode="w") as f:
                    f.write(self.public_key)
                    f.write("\n")
                    f.write(self.private_key)
                return True
            except (IOError, IndexError):
                print("Saving wallet failed...")
                return False

    def load_keys(self):
        try:
            with open("wallet.txt", mode="r") as f:
                keys = f.readlines()
                public_key = keys[0][:-1]
                private_key = keys[1]
                self.private_key = private_key
                self.public_key = public_key
            return True
        except (IOError, IndexError):
            print("Loading wallet failed...")
            return False

    def generate_keys(self):
        private_key = RSA.generate(1024, rn.new().read)
        public_key = private_key.publickey()
        # https://docs.python.org/2/library/binascii.html
        # https://www.dlitz.net/software/pycrypto/api/current/
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii'))

    def sign_transaction(self, sender, recipient, amount):
        """For signing transaction"""
        # Digital Signature - Create new signature object with private key (transaction will sign by private key and decrypt by public key)
        signer = PKCS1_v1_5.new(RSA.importKey(
            binascii.unhexlify(self.private_key)))
        h = SHA256.new((str(sender) + str(recipient) +
                        str(amount)).encode('utf8'))
        signature = signer.sign(h)
        return binascii.hexlify(signature).decode('ascii')

    @staticmethod
    def verify_transaction(transaction):
        # If put here: the transaction will verified when sender is `MINING`
        # if transaction.sender == 'MINING':
        #     return True

        public_key = RSA.importKey(binascii.unhexlify(transaction.sender))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA256.new((str(transaction.sender) + str(transaction.recipient) +
                        str(transaction.amount)).encode('utf8'))
        # Compare hash
        return verifier.verify(h, binascii.unhexlify(transaction.signature))
