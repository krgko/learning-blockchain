import hashlib as hl
import json

def hs256(string):
    return hl.sha256(string).hexdigest()

def hash_block(block):
    # like json stringify as digest because it will return as byte at initial
    # the order might changed and will make hashes invalid that is why we need to add sort
    return hs256(json.dumps(block, sort_keys=True).encode())
