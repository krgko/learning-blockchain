from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from blockchain import Blockchain
from wallet import Wallet

# Pass application name to tell context name to Flask
app = Flask(__name__)

CORS(app)

# TODO: Support totally multiple node on difference device


@app.route("/wallet", methods=['POST'])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)
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
        blockchain = Blockchain(wallet.public_key, port)
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


@app.route("/broadcast-transaction", methods=['POST'])
def broadcast_transaction():
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data found'
        }
        return jsonify(response), 400
    required = ['sender', 'recipient', 'amount', 'signature']
    if not all(key in values for key in required):
        response = {
            'message': 'Some data is missing'
        }
        return jsonify(response), 400
    # Add to transaction list
    success = blockchain.add_transaction(
        values['recipient'], values['sender'], values['signature'], values['amount'], is_receiving=True)
    if success:
        response = {
            'message': 'Added transaction success',
            'transaction': {
                'sender':  values['sender'],
                'recipient': values['recipient'],
                'amount': values['amount'],
                'signature': values['signature'],
            }
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Added transaction failed'
        }
        return jsonify(response), 500


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


@app.route("/broadcast-block", methods=["POST"])
def broadcast_block():
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data found'
        }
        return jsonify(response), 400
    if 'block' not in values:
        response = {'message': "Required data is missing"}
        return jsonify(response), 400
    block = values['block']
    # TODO: Auto catch up block both data and index
    if block['index'] == blockchain.chain[-1].index + 1:
        if blockchain.add_block(block):
            response = {'message': 'Block added'}
            return jsonify(response), 201
        else:
            response = {'message': 'Block invalid'}
            return jsonify(response), 409
    elif block['index'] > blockchain.chain[-1].index:
        # Blockchain shorter than current blockchain
        response = {
            'message': 'Blockchain differ from current blockchain'}
        blockchain.resolve_conflicts = True
        return jsonify(response), 200  # Not a problem
    else:
        response = {
            'message': 'Cannot add a block with index newer than the current block'}
        return jsonify(response), 409  # Data invalid


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
    # FIXME: Every loaded wallet the state will be cleared -> can attack like load-wallet, mine until blockchain longer than main blockchain
    if blockchain.resolve_conflicts:
        response = {
            'message': 'Resolve conflicts first, block cannot added'
        }
        return jsonify(response), 409
    # If does not have public_key it will failed
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


@app.route("/resolve-conflicts", methods=["POST"])
def resolve_conflicts():
    replaced = blockchain.resolve()
    if replaced:
        response = {'message': 'Chain was replaced'}
    else:
        response = {'message': 'Using local chain'}
    return jsonify(response), 200


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
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5000)
    args = parser.parse_args()  # Parse list of them
    port = args.port  # The argument name depends on --<variable> alias
    wallet = Wallet(port)
    blockchain = Blockchain(wallet.public_key, port)
    app.run(host="0.0.0.0", port=port)
