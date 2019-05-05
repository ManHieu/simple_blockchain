import requests
from flask import Flask, jsonify, request

from block import Block
from blockchain import Blockchain

app = Flask(__name__)
anchors = set()  # <ip>:<port>
anchors.add('127.0.0.1:5001')
orders = set()
orders.add('127.0.0.1:5002')
blockchain = Blockchain()


@app.route('/register')
def registe():
    global blockchain
    print("last blockchain :{}".format(blockchain.make_json()))

    data = {
        'port': 5000
    }

    longest_data_chain = []
    longest_lenth = 0

    for anchor in anchors:
        try:
            url = 'http://{}/add_node'.format(anchor)
            print("send data: {}".format(data))
            http_response = requests.post(url, json=data)
            print(http_response)
            response = http_response.json()  # {'chain':chain, 'len': len}
            data_chain = response['chain']
            print(data_chain)
            lenth = response['len']

            if lenth > longest_lenth:
                longest_data_chain = data_chain
                longest_lenth = lenth

        except:
            print("cannot connect anchor {}".format(anchor))
    
    print(longest_data_chain)
    blockchain = Blockchain.from_list(longest_data_chain)
    print("current blockchain :{}".format(blockchain.make_json()))
    return "sucess", 200


@app.route('/local_chain', methods=['GET','POST'])
def get_local_chain():
    chain_data = []

    for block in blockchain.chain:
        chain_data.append(block.__dict__)

    return jsonify({"len": len(chain_data), "chain": chain_data})


@app.route('/syn_chain', methods=['GET','POST'])
def syn_chain():
    global blockchain

    data = request.get_json()
    print("receive data: {}".format(data))
    data_chain = data['chain']

    blockchain = Blockchain.from_list(data_chain)
    print('after concensus: {}'.format(blockchain.make_json()))

    return "success", 200


@app.route('/add_block', methods=['GET','POST'])
def add_block():
    data = request.get_json()
    new_block = Block.from_dict(data)

    last_block = blockchain.get_last_block()

    if Blockchain.is_valid_block(new_block, last_block):
        blockchain.add_block(new_block)
        # print('invalid blockchain')
    
    print('new blockchain: {}'.format(blockchain.make_json()))
    
    return 'success', 200


@app.route('/deal', methods=['GET','POST'])
def get_transaction():
    pass

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    # print('My ip address : ' + get_ip())

    app.run(port=port, debug = True, threaded = True)

