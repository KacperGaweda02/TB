import hashlib
import json
from time import time


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = {
            "index": 1,
            "timestamp": 0,
            "transactions": [],
            "nonce": 0,
            "previous_hash": "0" * 64,
        }
        self.chain.append(genesis)

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, transactions):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": transactions,
            "nonce": 0,
            "previous_hash": self.hash(self.last_block),
        }
        self.chain.append(block)
        return block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block["previous_hash"] != self.hash(previous_block):
                return False, i
        return True, -1


if __name__ == "__main__":
    bc = Blockchain()
    bc.add_block(["Test1 -> Test2: 12"])
    bc.add_block(["Test3 -> Test4: 34"])
    bc.add_block(["Test5 -> Test6: 56"])
    for block in bc.chain:
        print(json.dumps(block, indent=2, ensure_ascii=False))
        print("hash:", Blockchain.hash(block))
        print("-" * 70)
    czy_poprawny, zepsuty_indeks = bc.is_chain_valid()
    if czy_poprawny:
        print(f"Czy łańcuch jest poprawny? {czy_poprawny}")
    else:
        print(f"Czy łańcuch jest poprawny? {czy_poprawny}\nHash bloku o indeksie {zepsuty_indeks} "
              f"różni się od atrybutu previous_hash w bloku o indeksie {zepsuty_indeks+1}")