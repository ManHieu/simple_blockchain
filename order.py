import requests
from flask import Flask

from block import Block
from blockchain import Blockchain

app = Flask(__name__)
uncomfirmed_transactions = ['Hiếu gửi Hiếu 1 BTC', 'Hiếu bán 1 BTC với giá 8097$',
                            'Hiếu dùng tiền mua 50 quyển sách và một máy đọc sách']
anchors = set()
anchors.add('127.0.0.1:5001')


@app.route('/mine', methods=['GET', 'POST'])
def mine():
    global last_block, uncomfirmed_transactions

    for anchor in anchors:
        try:
            url = 'http://{}/concensus'.format(anchor)
            http_response = requests.get(url)
            last_block = http_response.json()['last_block']
            last_hash = http_response.json()['last_hash']
        except:
            print("cannot connect anchor {}". format(anchor))

    previous_hash = last_hash
    difficult = last_block['difficult']
    transaction_counter = len(uncomfirmed_transactions)
    index = last_block['index'] + 1

    new_block = Block(
        index, previous_hash, 0, transaction_counter, difficult, uncomfirmed_transactions
    )

    uncomfirmed_transactions = []

    Blockchain.proof_of_work(new_block)

    for anchor in anchors:
        try:
            url = 'http://{}/broadcast_block'.format(anchor)
            http_response = requests.post(url, json=new_block.__dict__)
        except:
            print("cannot connect anchor {}". format(anchor))

    return 'success', 200


@app.route('/order', methods=['GET', 'POST'])
def line_up():
    pass


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5002,
                        type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    # print('My ip address : ' + get_ip())

    app.run(port=port, debug=True, threaded=True)
