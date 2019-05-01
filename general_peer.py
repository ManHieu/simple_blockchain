import requests
from flask import Flask, jsonify, request

from blockchain import Blockchain

app = Flask(__name__)
anchor_ip = '127.0.0.1' # sau này phải có phương thức để tìm
anchor_port = 5001
blockchain = Blockchain()

@app.route('/registe', methods=['POST', 'GET'])
def registe():
    data = {
        'port': 5000
    }

    try:
        url = 'http://{}:{}/add_node'.format(anchor_ip, anchor_port)
        # print(data)
        response = requests.post(url, json=data)
        print(response)
        return 'success', 200
    except:
        return "Cannot connect anchor", 400
    
@app.route('/add_block', methods=['POST', 'GET'])
def add_block():
    global blockchain
    data = request.get_json()

    block = Blockchain.create_new_block(
            data['nonce'], data['previous_block_hash'], data['difficult'], data['index'],
            data['transaction_counter'], data['transactions']
        )
    
    flag = blockchain.add_block(block)

    if flag == True:
        return 'success add block to block chain', 200
    else:
        return 'invalid block', 400

@app.route('/local_chain', methods=['GET'])
def get_local_chain():
    local_blockchain = blockchain.toDict()
    chain_data = local_blockchain['chain']
    return jsonify({"length": len(chain_data),
                       "chain": chain_data})

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    # print('My ip address : ' + get_ip())

    app.run(port=port, debug = True, threaded = True)
