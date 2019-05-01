import time
from block_header import Block_header
from block import Block


class Blockchain(object):

    difficult = 2

    def __init__(self):
        self.chain = []
        self.uncomfirmed_transactions = []
        self.create_genesis_block()

    def toDict(self):
        uncomfirmed_transactions = []
        chain = []
        for transaction in self.uncomfirmed_transactions:
            uncomfirmed_transactions.append(transaction)

        for block in self.chain:
            chain.append(block.toDict())

        block_chain = {
            'uncomfirmed_transactions': uncomfirmed_transactions,
            'chain': chain,
        }
        return block_chain

    @staticmethod
    def from_list(chain_data):
        chain = []
        for data in chain_data:
            block = Blockchain.create_new_block(data['nonce'], data['previous_block_hash'], data['difficult'],
                                                data['index'], data['transaction_counter'], data['transactions'])
            chain.append(block)

        return chain

    @staticmethod
    def create_new_block(nonce, previous_block_hash, difficult,
                         index, transaction_counter, transactions, timestamp=None):

        block_header = Block_header(nonce=nonce,
                                    previous_block_hash=previous_block_hash,
                                    difficult=difficult)

        block = Block(block_header=block_header,
                      index=index,
                    #   size=size,
                      transaction_counter=transaction_counter,
                      transactions=transactions)

        return block

    def create_genesis_block(self):
        genesis_block = self.create_new_block(nonce=0,
                                              previous_block_hash='0',
                                              difficult=Blockchain.difficult,
                                              index=0,
                                            # size=80,
                                              transaction_counter=0,
                                              transactions=[],)

        self.chain.append(genesis_block)

    def proof_of_work(self, block):
        block.block_header.nonce = 0

        hash = block.compute_hash()

        while not hash.startswith('0'*Blockchain.difficult):
            block.block_header.nonce += 1
            hash = block.compute_hash()

        return hash

    @staticmethod
    def is_valid_block(block, previous_block):
        if block.index - previous_block.index != 1:
            print("Sai ở 1")
            return False
        elif previous_block.compute_hash() != block.block_header.previous_block_hash:
            print("Sai ở 2")
            return False
        elif not block.compute_hash().startswith('0'*Blockchain.difficult):
            print("Sai ở 3")
            return False
        elif block.block_header.timestamp < previous_block.block_header.timestamp:
            print(block.block_header.timestamp)
            print(previous_block.block_header.timestamp)
            print("Sai ở 4")
            return False

        return True

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, block):
        previous_block = self.get_last_block()

        if self.is_valid_block(block, previous_block):
            self.chain.append(block)
            return True
        else:
            return False

    def is_valid_chain(self):
        """
        Check if given blockchain is valid
        """
        previous_block = self.chain[0]
        current_index = 1

        while current_index < len(self.chain):

            block = self.chain[current_index]

            if not self.is_valid_block(block, previous_block):
                return False

            previous_block = block
            current_index += 1

        return True

    def add_uncomfirm_transaction(self, transaction):
        self.uncomfirmed_transactions.append(transaction)
        return True

# test = Blockchain()
# last_block = test.get_last_block()
# hash1 = last_block.compute_hash()
# transactions = ["Hiếu"]
# block = test.create_new_block(0, hash1, 2, 1, 0, 1, transactions)
# hash2 = test.proof_of_work(block)
# # print(block.toDict())
# # print(hash1)
# # print(hash2)
# flag = test.add_block(block)
# test.add_uncomfirm_transaction("Hiếu")
# print(flag)
# print("Blockchain: {} \n {}".format(test.toDict(), test.is_valid_chain()))
