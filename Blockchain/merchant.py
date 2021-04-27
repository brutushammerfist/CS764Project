from block import Block
from customer import Customer
from transaction import Transaction

import random
import rsa

class Merchant:

    public_key: str
    private_key: str

    def __init__(self):
        (pub, priv) = rsa.newkeys(512)
        self.public_key = pub
        self.private_key = priv

    def sign(self, transaction: Transaction):
        transaction.merchant_signature = rsa.sign(transaction.merchant_signature_bytes(), self.private_key, 'SHA-256')

    def create_transaction(self, customer: Customer, date: str, amount: float) -> Transaction:
        new_transaction = Transaction(customer.public_key, self.public_key, date, amount)
        customer.sign(new_transaction)
        self.sign(new_transaction)
        return new_transaction