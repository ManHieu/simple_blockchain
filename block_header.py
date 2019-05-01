import time


class Block_header(object):
    def __init__(self, nonce, previous_block_hash, difficult, timestamp=None):
        self.previous_block_hash = previous_block_hash
        self.timestamp = timestamp or time.time()
        self.difficult = difficult 
        self.nonce = nonce
    
    def toDict(self):
        header = {
            'previous_block_hash': self.previous_block_hash,
            'nonce': self.nonce,
            'difficult': self.difficult,
            'timestamp': self.timestamp,
        }
        return header
    
    def __str__(self):
        return "{}{}{}{}".format(self.previous_block_hash, self.nonce, self.difficult, self.timestamp)

