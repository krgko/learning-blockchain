from Crypto.PublicKey import RSA
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
            except (IOError, IndexError):
                print("Saving wallet failed...")

    def load_keys(self):
        try:
            with open("wallet.txt", mode="r") as f:
                keys = f.readlines()
                public_key = keys[0][:-1]
                private_key = keys[1]
                self.private_key = private_key
                self.public_key = public_key
        except (IOError, IndexError):
            print("Loading wallet failed...")

    def generate_keys(self):
        private_key = RSA.generate(1024, rn.new().read)
        public_key = private_key.publickey()
        # https://docs.python.org/2/library/binascii.html
        # https://www.dlitz.net/software/pycrypto/api/current/
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii'))