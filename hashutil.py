import hashlib as hl
import json

def hs256(string):
    return hl.sha256(string).hexdigest()

# When change block as json to Block object it might be failed due to cannot convert to json
def hash_block(block):
    # like json stringify as digest because it will return as byte at initial
    # the order might changed and will make hashes invalid that is why we need to add sort
    hashable_block = block.__dict__.copy() # Copy of dict
    return hs256(json.dumps(hashable_block, sort_keys=True).encode())
