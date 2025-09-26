import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_tickets = []
        self.create_block(previous_hash="1")  # Genesis block

    def create_block(self, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'tickets': self.current_tickets,
            'previous_hash': previous_hash
        }
        block['hash'] = self.hash(block)
        self.current_tickets = []
        self.chain.append(block)
        return block

    def add_ticket(self, event_id, ticket_id, owner):
        # Each ticket is unique
        ticket = {
            'event_id': event_id,
            'ticket_id': ticket_id,
            'owner': owner,
            'redeemed': False
        }
        self.current_tickets.append(ticket)
        return ticket

    def redeem_ticket(self, ticket_id):
        for block in self.chain:
            for t in block['tickets']:
                if t['ticket_id'] == ticket_id:
                    if t['redeemed']:
                        return False
                    t['redeemed'] = True
                    return True
        return False

    def verify_ticket(self, ticket_id, event_id):
        for block in self.chain:
            for t in block['tickets']:
                if t['ticket_id'] == ticket_id:
                    if t['event_id'] != event_id:
                        return {"valid": False, "reason": "wrong_event"}
                    if t['redeemed']:
                        return {"valid": False, "reason": "already_redeemed"}
                    return {"valid": True, "owner": t['owner']}
        return {"valid": False, "reason": "not_found"}

    @staticmethod
    def hash(block):
        block_copy = dict(block)
        block_copy.pop('hash', None)
        return hashlib.sha256(json.dumps(block_copy, sort_keys=True).encode()).hexdigest()
