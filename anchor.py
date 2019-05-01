"""
anchor peer
quản lý các general peer trong tổ chức 
thực hiện các chức năng: 
- thêm general peer
- phân quyền các peer (?)
- nhận block từ order node và broad cast block cho các general peer
- concensus giữa các general peer
"""

import requests
from flask import Flask, jsonify, request

from blockchain import Blockchain

app = Flask(__name__)
peer_list = set()


@app.route('/add_node', methods=['GET', 'POST'])
def validate_conection():
    # print(request)
    data = request.get_json()
    # print(data)

    if not data:
        return 'invalid', 400

    request_addr = request.remote_addr
    node = str(request_addr) + ':' + str(data['port'])

    peer_list.add(node)
    print(peer_list)
    return 'success', 200

# def get_peer_list():
#     print(peer_list)


@app.route('/broadcast_block', methods=['GET', 'POST'])
def broadcast():
    data = request.get_json()
    try:
        block = Blockchain.create_new_block(
            data['nonce'], data['previous_block_hash'], data['difficult'], data['index'],
            data['transaction_counter'], data['transactions']
        )
    except:
        return 'invalid data', 400

    for peer in peer_list:
        try:
            url = "http://{}/add_block".format(peer)
            requests.post(url, json=data)

        except requests.exceptions.ConnectionError:
            print('Cant connect to node {}. Remove it from peers list'.format(peer))
            peer_list.remove(peer)

    return "Success", 200


@app.route('/concensus', methods=['GET'])
def reach_concensus():
    current_len = 0
    current_chain = []
    for peer in peer_list:
        try:
            response = requests.get('http://{}/local_chain'.format(peer))
            lenth = response.get_json()['length']
            chain_data = response.get_json()['chain']
            chain = Blockchain.from_list(chain_data)
            block_chain = Blockchain()
            block_chain.chain = chain
            
            if current_len < lenth and block_chain.is_valid_chain():
                current_len = lenth
                current_chain = chain

        except requests.exceptions.ConnectionError:
            print('Cant connect to node {}. Remove it from peers list'.format(peer))
            peer_list.remove(peer)
        
        return jsonify({"length": current_len,
                       "chain": current_chain})


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001,
                        type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    # print('My ip address : ' + get_ip())

    app.run(port=port, debug=True, threaded=True)
