from Crypto.PublicKey import RSA
import Crypto.Random as rn
import binascii


class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        """ Keypair will create from this method only """
        private_key, private_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = private_key

    def load_keys(self):
        pass

    def generate_keys(self):
        private_key = RSA.generate(1024, rn.new().read)
        public_key = private_key.publickey()
        # https://docs.python.org/2/library/binascii.html
        # https://www.dlitz.net/software/pycrypto/api/current/
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii'))
