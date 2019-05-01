import hashlib


class Block(object):
    def __init__(self, block_header, index, transaction_counter, transactions):
        self.block_header = block_header
        self.index = index
        self.transaction_counter = transaction_counter
        self.transactions = transactions
        # self.size = size

    def compute_hash(self):
        # print(self.block_header)
        block_string = "{}{}{}{}".format(self.block_header, self.index,
                                           self.transactions, self.transaction_counter)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def toDict(self):
        block = {
            'block_header': self.block_header.toDict(),
            'index': self.index,
            'transaction_counter': self.transaction_counter,
            # 'size': self.size,
            'transactions': self.transactions,
        }
        return block
    

