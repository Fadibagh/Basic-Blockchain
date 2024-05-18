from block import Block
from transactions import Transaction

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

        # generating first block in the block chain
        genesis_block = Block(0,[],"0")
        self.chain.append(genesis_block)

    def add_block(self):
        """Adds a new block to the end of the chain
        
        Args: 
            transactions: a list transactions within grouped together to be added to a new block
        """
        previous_hash = self.chain[-1].hash

        new_block = Block(len(self.chain), self.pending_transactions, previous_hash)
        self.chain.append(new_block)
        self.pending_transactions = []

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.recipient == address:
                    balance += transaction.amount
        return balance

    def add_transaction(self, sender, recipient, amount):
        transaction = Transaction(sender, recipient, amount)
        self.pending_transactions.append(transaction)

    def is_chain_valid(self):
        """Checking if the chain is intact and not changed
         
        Returns:
            True: if chain is valid
            False: if chain is invalid
        """


        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.compute_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False
            
        return True
    
    def __repr__(self):
        return f"Blockchain(chain={self.chain})"

    

            
            

    