from block import Block
from blockchain import Blockchain
from customer import Customer
from merchant import Merchant
from transaction import Transaction

import rsa

class MinerNode:
    blockchain: Blockchain

    public_key: str
    private_key: str
    difficulty: int

    def __init__(self, difficulty):
        self.blockchain = Blockchain(difficulty)

        (pub, priv) = rsa.newkeys(512)
        self.public_key = pub
        self.private_key = priv
        self.difficulty = difficulty

    def sign(self, block: Block):
        block.miner_signature = rsa.sign(block.miner_signature_bytes(), self.private_key, 'SHA-256')

    def add_block(self, transaction: Transaction):
        new_block = self.blockchain.create_new_block(transaction)
        self.sign(new_block)
        self.blockchain.add_block(new_block)

    def display(self):
        self.blockchain.display()

    def increment_fifteen(self):
        print("Incrementing transaction 15 amount by 10.")
        self.blockchain.increment_fifteen()

    def is_chain_valid(self) -> bool:
        return self.blockchain.is_chain_valid()

    def print_customer_three(self, customer_three: Customer):
        print("Print Customer 3 Transactions:")
        self.blockchain.print_customer_three(customer_three)

    def print_merchant_two(self, merchant_two: Merchant):
        print("Print Merchant 2 Transactions:")
        self.blockchain.print_merchant_two(merchant_two)

    def output_to_file(self, filename: str):
        self.blockchain.output_to_file(filename)