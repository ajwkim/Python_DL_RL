import time, random, json, hashlib
from flask import Flask, request, jsonify

PROBLEM = '0'
DIFFICULTY = 4

def _hash(block):       # hashes a block
    block_str = json.dumps(block, sort_keys=True)
    return hashlib.sha256(block_str.encode()).hexdigest()

def valid_proof(last_proof, proof):
    guess = str(last_proof + proof)
    guess_hash = hashlib.sha256(guess.encode()).hexdigest()
    return guess_hash[:DIFFICULTY] == PROBLEM * DIFFICULTY

def valid_chain(chain):
    return all(block['previous_hash'] == _hash(last_block)
               for last_block, block in zip(chain, chain[1:]))

def _pow(last_proof):
    while not valid_proof(last_proof, proof:=random.randrange(-100_0000, 100_0001)):
        pass
    return proof


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)

    @property
    def last_block(self):
        return self.chain[-1]
    
    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append(
            dict(sender=sender, recipient=recipient, amount=amount, timestamp=time.time()))
        return self.last_block['index'] + 1
    
    def new_block(self, proof, previous_hash=None):
        block = dict(index=len(self.chain)+1,                               # 1, 2, 3, ...
                     timestamp=time.time(),
                     transactions=self.current_transactions,
                     nonce=proof,
                     previous_hash=previous_hash or _hash(self.last_block))
        self.chain.append(block)
        self.current_transactions = []
        return block
    

blockchain = Blockchain()
myip = '127.0.0.1'
myport = '5000'
node_identifier = 'node_' + myport
mine_owner = 'master'
mine_profit = .1

app = Flask(__name__)

@app.route('/chain', methods=['GET'])
def full_chain():
    print('\nchain info requested!')
    response = dict(chain=blockchain.chain, length=len(blockchain.chain))
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    print('\ntransactions_new!!!:', values)
    required = 'sender recipient amount'.split()
    if not all(k in values for k in required):
        return 'missing values', 400
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = dict(message=f'Transaction will be added to Block {index}')
    return jsonify(response), 201

@app.route('/mine', methods=['GET'])
def mine():
    print('\nMINING STARTED')
    last_proof = blockchain.last_block['nonce']
    proof = _pow(last_proof)

    blockchain.new_transaction(sender=mine_owner, recipient=node_identifier, amount=mine_profit)
    block = blockchain.new_block(proof)
    print('MINING FINISHED')
    response=dict(message='new block found', 
                  index=block['index'],
                  transactions=block['transactions'],
                  nonce=block['nonce'],
                  previous_hash=block['previous_hash'])
    return jsonify(response), 200

app.run(host=myip, port=myport)