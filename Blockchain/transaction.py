import rsa

class Transaction:

    customer_public_key: rsa.PublicKey
    merchant_public_key: rsa.PublicKey
    date: str
    amount: float
    customer_signature: bytes
    merchant_signature: bytes

    def __init__(self, customer_key: rsa.PublicKey, merchant_key: rsa.PublicKey, date: str, amount: float):
        self.customer_public_key = customer_key
        self.merchant_public_key = merchant_key
        self.date = date
        self.amount = amount

    def customer_signature_bytes(self) -> bytes:
        return (str(self.customer_public_key) + str(self.merchant_public_key) + str(self.date) + str(self.amount)).encode('utf-8')

    def merchant_signature_bytes(self) -> bytes:
        return (str(self.customer_public_key) + str(self.merchant_public_key) + str(self.date) + str(self.amount) + str(self.customer_signature)).encode('utf-8')