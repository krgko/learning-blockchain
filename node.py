from flask import Flask, jsonify
from flask_cors import CORS

from blockchain import Blockchain
from wallet import Wallet

# Pass application name to tell context name to Flask
app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)

CORS(app)


@app.route("/wallet", methods=['POST'])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()

        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Saving key-pair failed',
        }
        return jsonify(response), 500


@app.route("/wallet", methods=['GET'])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()

        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'Loading key-pair failed',
        }
        return jsonify(response), 500


@app.route("/balance", methods=['GET'])
def get_balance():
    balance = blockchain.get_balance()
    if balance != None:
        response = {
            'message': 'Fetched balance successfully',
            'funds': balance
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'Getting balance failed',
            'wallet_set_up': wallet.public_key != None
        }
        return jsonify(response), 500


@app.route("/", methods=['GET'])
def get_ui():
    return 'UI showing!'


@app.route("/mine", methods=['POST'])
def mine():
    # If does not have node_id it will failed
    block = blockchain.mine_block()
    if block is not None:
        dict_block = block.__dict__.copy()
        dict_block['transactions'] = [
            tx.__dict__ for tx in dict_block['transactions']]
        response = {
            'message': 'Block added successfully',
            "block": dict_block,
            "funds": blockchain.get_balance()
        }
        # Created new resource
        return jsonify(response), 201
    else:
        response = {
            'message': 'Adding a block failed',
            'wallet_set_up': wallet.public_key != None
        }
        return jsonify(response), 500


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
