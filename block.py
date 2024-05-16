import hashlib
import datetime
import json

class Block:
    def __init__(self, index, transactions, previous_hash):
        """Constructor for Block class
        
        Args: 
            index: index of block in the blockchain
            transactions: list of all transactions in the block chain
            previous_hash: hash of the previous entry in the block chain

        """

        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = datetime.datetime.now()
        self.nonce = 0 
        self.hash = self.compute_hash()

    def compute_hash(self):
        """Method to compute the hash of the block
        
        Args:
            self
        
        Returns: returns a hash of the contents of the block
        
        """

        block_string = json.dumps(self.__dict__, default=str, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def __str__(self):
        """Helper method to print the contents of the block easily"""
        transactions_string = ', '.join(sorted(str(tx) for tx in self.transactions))
        return (f"Block(Index :{self.index}, Timestamp: {self.timestamp}, Transactions: {transactions_string}, Previous Hash: {self.previous_hash}, Hash: {self.hash}, Nonce: {self.nonce}")
    
    def __repr__(self):
        return (f"Block(index={self.index}, transactions={self.transactions}, "
                f"previous_hash='{self.previous_hash}', timestamp={self.timestamp}, "
                f"hash='{self.hash}')")
    
    def to_dict(self):
        """Convert block instance into a dictionary format that can be JSON serialized."""
        return {
            "index": self.index,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp.isoformat(),  # ISO format datetime string
            "nonce": self.nonce,
            "hash": self.hash
        }
    


        