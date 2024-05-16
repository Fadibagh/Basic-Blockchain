import unittest

from block import Block
from blockchain import Blockchain

class TestBlock(unittest.TestCase):

    def setUp(self):
        self.transactions = ["first transaction", "second transaction", "third transaction"]
        self.block = Block(1, self.transactions, "0")

    def test_block_hash(self):

        initial_hash = self.block.hash
        self.assertIsNotNone(initial_hash)
        self.assertEqual(self.block.compute_hash(), initial_hash)

    def test_block_data_change(self):

        # changing transactions
        self.block.transactions = ["fourth transaction", "fifth transaction", "sixth transaction"]
        new_hash = self.block.compute_hash()
        self.assertNotEqual(self.block.hash, new_hash)

    def test_transaction_order_impact(self):

        expected_hash = self.block.hash
        self.block.transactions = ["third transaction", "second transaction", "first transaction"]
        self.block.hash = self.block.compute_hash()  
        self.assertNotEqual(self.block.hash, expected_hash)

    def test_block_str(self):
        block = Block(1, "sample transaction", "0")
        self.assertIn("Block(Index :1", str(block))


class TestBlockchain(unittest.TestCase):

    def setUp(self):
        self.blockchain = Blockchain()

    def test_adding_block(self):
        transactions = ['1', '2', '3']

        self.blockchain.add_block(transactions)

        self.assertEqual(len(self.blockchain.chain), 2)

        new_block = self.blockchain.chain[-1]

        self.assertEqual(transactions, new_block.transactions, "Transactions do not match")

        self.assertEqual(new_block.previous_hash, self.blockchain.chain[0].hash, "Newblock's previous hash does not match genesis block hash")

        self.assertEqual(new_block.index, 1, "Unexpected index")

    def test_blockchain_validaty(self):
        self.blockchain.add_block(["t1"])
        self.blockchain.add_block(["t2"])
        self.assertTrue(self.blockchain.is_chain_valid())

    def test_blockchain_tampering(self):
        self.blockchain.add_block(['t1'])
        self.blockchain.add_block(["t2"])

        self.blockchain.chain[1].transactions = ["tampered transactions"]

        self.blockchain.chain[1].hash = self.blockchain.chain[1].compute_hash()

        self.assertFalse(self.blockchain.is_chain_valid())


if __name__ == '__main__':
    unittest.main()