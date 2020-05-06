from flask import Flask, jsonify
from flask_cors import CORS

from blockchain import Blockchain
from wallet import Wallet

# Pass application name to tell context name to Flask
app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)

CORS(app)

# No class here
@app.route("/", methods=['GET'])
def get_ui():
    return 'UI showing!'


@app.route("/chain", methods=["GET"])
def get_chain():
    # Cannot use this plainly because the variable will not be dict type so, it will not json.loads
    chain_snapshot = blockchain.chain
    # .copy() to copy whole dict
    # Example from hashutil.py
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    for dict_block in dict_chain:
        dict_block['transactions'] = [
            tx.__dict__ for tx in dict_block["transactions"]]
    return jsonify(dict_chain), 200


if __name__ == "__main__":
    # flask: https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application
    # flask_cors: https://flask-cors.readthedocs.io/en/latest/
    app.run(host="0.0.0.0", port=5000)
