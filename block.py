from bitstring import BitArray
import time
from transaction import Transaction

import hashlib

class Block:
    block_seq_number: int
    previous_hash: str
    miner_signature: bytes
    nonce: BitArray
    difficulty: int
    nonces_tried: int
    time_to_calc: float
    curr_hash: bytes
    
    transaction: Transaction

    def __init__(self, seq_number: int, previous_hash: str, transaction: Transaction, difficulty: int):
        self.block_seq_number = seq_number
        self.previous_hash = previous_hash
        self.transaction = transaction
        self.difficulty = difficulty
        self.nonce = BitArray(uint=0, length=128)
        self.nonces_tried = 0
        self.time_to_calc = 0
        self.curr_hash = self.calculate_hash()

    def miner_signature_bytes(self) -> bytes:
        return (str(self.transaction.merchant_signature) + str(self.block_seq_number) + str(self.previous_hash)).encode('utf-8')

    def calculate_hash(self) -> bytes:
        curr_hash = b''
        start_time = time.time()

        if(self.difficulty == 0):
            if self.block_seq_number == 0:
                curr_hash = hashlib.sha256(self.nonce.tobytes() + "0000000".encode('utf-8')).digest()
            else:
                curr_hash =  hashlib.sha256((self.nonce.tobytes() + (str(self.transaction.customer_public_key) + str(self.transaction.merchant_public_key) + str(self.transaction.date) + str(self.transaction.amount) + str(self.transaction.customer_signature) + str(self.transaction.merchant_signature) + str(self.block_seq_number)).encode('utf-8'))).digest()
            self.nonces_tried += 1
        else:
            print(str(BitArray(bytes=curr_hash).bin))
            while(not (str(BitArray(bytes=curr_hash).bin).startswith("0"*self.difficulty))):
                if self.block_seq_number == 0:
                    curr_hash = hashlib.sha256(self.nonce.tobytes() + "0000000".encode('utf-8')).digest()
                else:
                    curr_hash = hashlib.sha256((self.nonce.tobytes() + (str(self.transaction.customer_public_key) + str(self.transaction.merchant_public_key) + str(self.transaction.date) + str(self.transaction.amount) + str(self.transaction.customer_signature) + str(self.transaction.merchant_signature) + str(self.block_seq_number)).encode('utf-8'))).digest()
                self.nonce = BitArray(uint=(self.nonce.uint + 1), length=128)
                self.nonces_tried += 1

        self.time_to_calc = time.time() - start_time
        return curr_hash

    def display(self):
        print("---------------------------")
        print("Customer Public Key: " + str(self.transaction.customer_public_key))
        print("Merchant Public Key: " + str(self.transaction.merchant_public_key))
        print("Date: " + str(self.transaction.date))
        print("Amount: " + str(self.transaction.amount))
        print("---------------------------")

    def string_to_output(self) -> str:
        to_output = ""
        if self.difficulty == 0:
            to_output += "A,"
        elif self.difficulty == 5:
            to_output += "B,"
        elif self.difficulty == 10:
            to_output += "C,"
        to_output += str(self.block_seq_number) + "," + str(self.nonces_tried) + "," + str(self.time_to_calc)

        return to_output