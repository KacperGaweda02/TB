from argparse import ArgumentParser
from uuid import uuid4
from flask import Flask, jsonify, request
from blockchain import Blockchain

app = Flask(__name__)
node_identifier = str(uuid4()).replace("-", "")
blockchain = Blockchain()


@app.get("/chain")
def full_chain():
    return jsonify({"chain": blockchain.chain, "length": len(blockchain.chain)}), 200


@app.post("/transactions/new")
def new_transaction():
    values = request.get_json(silent=True)
    if values is None:
        return jsonify({"error": "Treść nie jest poprawnym formatem JSON"}), 400

    required_keys = {"sender", "recipient", "amount"}
    if set(values.keys()) != required_keys:
        return jsonify({"error": "Wymagane sa dokladnie pola: sender, recipient, amount (bez dodatkowych)"}), 400

    sender = values["sender"]
    recipient = values["recipient"]
    amount = values["amount"]

    if sender == recipient:
        return jsonify({"error": "Nadawca i odbiorca nie moga byc tacy sami"}), 400

    if not isinstance(amount, (int, float)) or isinstance(amount, bool):
        return jsonify({"error": "Kwota musi byc liczba"}), 400

    if amount <= 0:
        return jsonify({"error": "Kwota musi byc wieksza od zera"}), 400

    if amount > 1_000_000:
        return jsonify({"error": "Przekroczono maksymalna dozwolona kwote transakcji"}), 400

    index = blockchain.new_transaction(sender, recipient, amount)
    return jsonify({"message": f"Transakcja zostanie dodana do bloku {index}"}), 201


@app.post("/mine")
def mine():
    block = blockchain.mine(node_identifier)
    return jsonify({
        "message": "Wydobyto nowy blok",
        "block": block,
        "hash": blockchain.hash(block),
    }), 200


@app.get("/transactions/pending")
def pending_transactions():
    return jsonify({
        "transactions": blockchain.current_transactions,
        "length": len(blockchain.current_transactions)
    }), 200


@app.get("/block/<int:index>")
def get_block(index):
    for block in blockchain.chain:
        if block["index"] == index:
            return jsonify(block), 200

    return jsonify({"error": "Blok nie istnieje"}), 404


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", default=5000, type=int)
    args = parser.parse_args()
    app.run(host="127.0.0.1", port=args.port)