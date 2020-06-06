from flask import Flask, jsonify, request, send_from_directory
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
    return send_from_directory('public', 'index.html')


@app.route("/network", methods=['GET'])
def get_network_ui():
    return send_from_directory('public', 'network.html')


@app.route("/transaction", methods=["POST"])
def add_transaction():
    if wallet.public_key == None:
        response = {
            'message': "No wallet setup"
        }
        return jsonify(response), 400
    # Get input as dict
    body = request.get_json()
    if not body:
        response = {'message': "No data input"}
        return jsonify(response), 400
    required_fields = ['recipient', 'amount']
    # Check required_fields are in json body
    if not all(field in body for field in required_fields):
        response = {'message': "Required data is missing"}
        return jsonify(response), 400
    # FIXME: Input type validation
    recipient = body['recipient']
    amount = int(body['amount'])
    signature = wallet.sign_transaction(wallet.public_key, recipient, amount)
    success = blockchain.add_transaction(
        recipient, wallet.public_key, signature, amount)
    if success:
        response = {
            'message': 'Added transaction success',
            'transaction': {
                'sender': wallet.public_key,
                'recipient': recipient,
                'amount': amount,
                'signature': signature,
            },
            'funds': blockchain.get_balance(),
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Added transaction failed'
        }
        return jsonify(response), 500


@app.route("/transactions", methods=['GET'])
def get_open_transactions():
    if wallet.public_key == None:
        response = {
            'message': "No wallet setup"
        }
        return jsonify(response), 400

    open_transactions = blockchain.get_open_transactions()
    open_transactions_dict = [tx.__dict__ for tx in open_transactions]
    return jsonify(open_transactions_dict), 200


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


@app.route("/node", methods=["POST"])
def add_node():
    body = request.get_json()
    if not body:
        response = {'message': 'No body attached'}
        return jsonify(response), 400
    # Check existance of key
    if 'node' not in body:
        response = {'message': 'No node data attached'}
        return jsonify(response), 400
    node = body['node']
    # Not required public key of wallet
    blockchain.add_peer_node(node)
    response = {
        'message': 'Node added successfully',
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 201


@app.route("/node/<node_url>", methods=["DELETE"])
def remove_node(node_url):
    if node_url == '' or node_url == None:
        response = {'message': 'No node found'}
        return jsonify(response), 400
    blockchain.remove_peer_node(node_url)
    response = {
        'message': 'Node removed',
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 200


@app.route("/nodes", methods=["GET"])
def get_nodes():
    nodes = blockchain.get_peer_nodes()
    response = {
        'all_nodes': nodes
    }
    return jsonify(response), 200


if __name__ == "__main__":
    # flask: https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application
    # flask_cors: https://flask-cors.readthedocs.io/en/latest/
    app.run(host="0.0.0.0", port=5000)
