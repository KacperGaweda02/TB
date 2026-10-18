import hashlib
import json
from time import time


class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = []
        self.current_transactions = []
        self.difficulty = difficulty
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

    def new_transaction(self, sender, recipient, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Kwota transakcji musi być liczbą dodatnią.")

        if not isinstance(sender, str) or not sender.strip():
            raise ValueError("Nadawca musi być niepustym ciągiem znaków.")

        if not isinstance(recipient, str) or not recipient.strip():
            raise ValueError("Odbiorca musi być niepustym ciągiem znaków.")

        if sender == recipient:
            raise ValueError("Nadawca i odbiorca nie mogą być tacy sami.")

        if sender != "0" and self.get_balance(sender) < amount:
            raise ValueError("Odrzucono: Brak wystarczających środków na koncie nadawcy.")

        self.current_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
        })
        return self.last_block["index"] + 1

    def proof_of_work(self, block):
        block["nonce"] = 0
        computed_hash = self.hash(block)
        while not computed_hash.startswith("0" * self.difficulty):
            block["nonce"] += 1
            computed_hash = self.hash(block)
        return computed_hash

    def mine(self, miner_address):
        reward = {"sender": "0", "recipient": miner_address, "amount": 1}

        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": [reward] + self.current_transactions,
            "nonce": 0,
            "previous_hash": self.hash(self.last_block),
        }

        self.proof_of_work(block)

        self.current_transactions = []
        self.chain.append(block)
        return block

    def valid_chain(self, chain):
        if chain[0] != self.chain[0]:
            return False
        for i in range(1, len(chain)):
            previous_block = chain[i - 1]
            current_block = chain[i]

            if current_block["previous_hash"] != self.hash(previous_block):
                return False
            if not self.hash(current_block).startswith("0" * self.difficulty):
                return False
        return True

    def get_balance(self, address):
        balance = 0

        for block in self.chain:
            for tx in block['transactions']:
                if tx['recipient'] == address:
                    balance += tx['amount']
                if tx['sender'] == address:
                    balance -= tx['amount']

        for tx in self.current_transactions:
            if tx['recipient'] == address:
                balance += tx['amount']
            if tx['sender'] == address:
                balance -= tx['amount']

        return balance


# if __name__ == "__main__":
#     bc = Blockchain(difficulty=4)
#
#     bc.new_transaction("Test1", "Test2", 12)
#     bc.new_transaction("Test3", "Test4", 34)
#     bc.mine("Gornik_1")
#
#     bc.new_transaction("Test5", "Test6", 56)
#     bc.mine("Gornik_1")
#
#     bc.mine("Gornik_1")
#
#     for block in bc.chain:
#         print(f"Index: {block['index']}, Nonce: {block['nonce']}, Hash: {bc.hash(block)}")

# if __name__ == "__main__":
#     wyniki = []
#
#     for d in range(1, 7):
#         bc = Blockchain(difficulty=d)
#
#         liczba_blokow = 5 if d < 6 else 2
#
#         suma_czasu = 0
#         suma_nonce = 0
#
#         print(f"\nRozpoczęto kopanie dla trudności: {d} (liczba bloków: {liczba_blokow})")
#
#         for i in range(liczba_blokow):
#             start_czas = time()
#             wykopany_blok = bc.mine("Gornik_Testowy")
#             koniec_czas = time()
#
#             czas_kopania = koniec_czas - start_czas
#             suma_czasu += czas_kopania
#             suma_nonce += wykopany_blok['nonce']
#             print(f" - Blok {i + 1} wykopany w {czas_kopania:.4f}s z nonce: {wykopany_blok['nonce']}")
#
#         sredni_czas = suma_czasu / liczba_blokow
#         sredni_nonce = suma_nonce / liczba_blokow
#
#         wyniki.append((d, sredni_nonce, sredni_czas))
#
#     print("Trudność | Średni nonce | Średni czas [s]")
#     for w in wyniki:
#         print(f"    {w[0]}    |    {w[1]:.0f}     |   {w[2]:.4f}")

# import matplotlib.pyplot as plt
#
# trudnosc = [1, 2, 3, 4, 5, 6]
# teoretyczna_liczba_prob = [16, 256, 4096, 65536, 1048576, 16777216]
# sredni_nonce = [12, 255, 5909, 73409, 999677, 14332492]
#
# plt.figure(figsize=(10, 6))
#
# plt.plot(trudnosc, teoretyczna_liczba_prob, marker='o', linestyle='-', color='blue', label='Teoretyczna liczba prób (16^d)')
# plt.plot(trudnosc, sredni_nonce, marker='s', linestyle='--', color='red', label='Średnia wartość nonce (empiryczna)')
#
# plt.yscale('log')
#
# plt.xlabel('Trudność (liczba wiodących zer)')
# plt.ylabel('Liczba prób / Nonce (skala logarytmiczna)')
# plt.title('Porównanie teoretycznej liczby prób ze średnią wartością nonce')
# plt.grid(True, which="both", ls="--", linewidth=0.5)
# plt.legend()
#
# plt.savefig('wykres_trudnosci.png', dpi=300)
# plt.show()

# if __name__ == "__main__":
#     bc = Blockchain(difficulty=4)
#
#     print("--- Wydobywanie 5 bloków ---")
#     for i in range(5):
#         bc.new_transaction(f"Nadawca_{i}", f"Odbiorca_{i}", 100)
#         wykopany_blok = bc.mine("Gornik_1")
#         print(f"Wykopano blok nr {wykopany_blok['index']}")
#
#     czy_poprawny_przed = bc.valid_chain(bc.chain)
#     print(f"\nCzy łańcuch przed modyfikacją jest poprawny? {czy_poprawny_przed}")
#
#     stara_kwota = bc.chain[1]["transactions"][1]["amount"]
#     bc.chain[1]["transactions"][1]["amount"] = 99999
#
#     print(f"\n--- Atak na blok nr 2 ---")
#     print(f"Zmieniono kwotę w bloku nr 2 z {stara_kwota} na 99999")
#
#     czy_poprawny_po = bc.valid_chain(bc.chain)
#     print(f"Czy łańcuch po modyfikacji jest poprawny? {czy_poprawny_po}")

# if __name__ == "__main__":
#     def symuluj_atak(bc, indeks_poczatkowy):
#         start_czas = time()
#
#         for i in range(indeks_poczatkowy, len(bc.chain)):
#             if i > indeks_poczatkowy:
#                 bc.chain[i]["previous_hash"] = bc.hash(bc.chain[i - 1])
#
#             bc.proof_of_work(bc.chain[i])
#
#         koniec_czas = time()
#         return koniec_czas - start_czas
#
#
#     for diff in [4, 5]:
#         print(f"\n=== Przygotowanie i atak dla trudności: {diff} ===")
#         bc = Blockchain(difficulty=diff)
#
#         for i in range(5):
#             bc.new_transaction(f"Nadawca_{i}", f"Odbiorca_{i}", 100)
#             bc.mine("Gornik_1")
#         print("Wykopano 5 poprawnych bloków.")
#
#         bc.chain[1]["transactions"][1]["amount"] = 99999
#         print("Sfałszowano transakcję w bloku nr 2.")
#
#         print(f"Łańcuch poprawny przed symulacją pracy? {bc.valid_chain(bc.chain)}")
#
#         print("Atakujący rozpoczyna przeliczanie łańcucha...")
#         czas_ataku = symuluj_atak(bc, 1)
#
#         print(f"Atak zakończony w czasie: {czas_ataku:.4f} s")
#         print(f"Łańcuch poprawny po ataku? {bc.valid_chain(bc.chain)}")