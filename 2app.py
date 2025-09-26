pip install flask
python app.py

from flask import Flask, request, jsonify
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/create_event', methods=['POST'])
def create_event():
    data = request.json
    event_id = data.get('event_id')
    return jsonify({"message": f"Event {event_id} created"}), 201

@app.route('/mint_ticket', methods=['POST'])
def mint_ticket():
    data = request.json
    ticket = blockchain.add_ticket(
        event_id=data['event_id'],
        ticket_id=data['ticket_id'],
        owner=data['owner']
    )
    blockchain.create_block(previous_hash=blockchain.chain[-1]['hash'])
    return jsonify(ticket), 201

@app.route('/verify/<ticket_id>/<event_id>', methods=['GET'])
def verify(ticket_id, event_id):
    result = blockchain.verify_ticket(ticket_id, event_id)
    return jsonify(result), 200

@app.route('/redeem/<ticket_id>', methods=['POST'])
def redeem(ticket_id):
    success = blockchain.redeem_ticket(ticket_id)
    return jsonify({"redeemed": success}), 200

if __name__ == '__main__':
    app.run(debug=True)
