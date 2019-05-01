import requests
from flask import Flask, jsonify

from blockchain import Blockchain

app = Flask(__name__)
anchor_ip = ''
anchor_port = ''

blockchain = Blockchain()
# uncomfirmed_transactions = []
uncomfirmed_transactions = blockchain.uncomfirmed_transactions


@app.route('/mine')
def mine():
    global blockchain, uncomfirmed_transactions
    number_of_transactions = len(uncomfirmed_transactions)
    if number_of_transactions == 0:
        return jsonify({'result': 'None transaction'})
    elif number_of_transactions < 10:
        return jsonify({'result': 'Not enough transaction for block. Please wait!'})

    last_block = blockchain.get_last_block()

    new_block = Blockchain.create_new_block(
        nonce=0,
        previous_block_hash=last_block.block_header.previous_block_hash,
        difficult=Blockchain.difficult,
        index=last_block.index + 1,
        # size=80,
        transaction_counter=number_of_transactions,
        transactions=[],
    )

    for transaction in uncomfirmed_transactions:
        new_block.transactions.append(transaction)

    uncomfirmed_transactions = []
    blockchain.uncomfirmed_transactions = []

    blockchain.proof_of_work(new_block)
    blockchain.add_block(new_block)


    try:
        url = 'http://{}/broadcast_block'.format(anchor_ip + ':' + anchor_port)
        data = new_block.toDict()
        requests.post(url, json=data)
    except:
        pass    
