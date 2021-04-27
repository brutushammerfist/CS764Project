from block import Block
from transaction import Transaction

import rsa

class Customer:
    public_key: rsa.PublicKey
    private_key: rsa.PrivateKey

    def __init__(self):
        (pub, priv) = rsa.newkeys(512)
        self.public_key = pub
        self.private_key = priv

    def sign(self, transaction: Transaction):
        transaction.customer_signature = rsa.sign(transaction.customer_signature_bytes(), self.private_key, 'SHA-256')