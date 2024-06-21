import time, random, json, hashlib, requests
from urllib.parse import urlparse
from flask import Flask, request, jsonify

PROBLEM = '0'
DIFFICULTY = 4
myip = '127.0.0.1'
myport = '5000'                                 # '5000', '5001', '5002'
mynode = f'{myip}:{myport}'                     # '127.0.0.1:5000'
node_identifier = 'node_' + myport
mine_owner, mine_profit = 'master', .1

def _sha(x):
    return hashlib.sha256(x.encode()).hexdigest()

def _hash(block):           # hashes a block
    return _sha(json.dumps(block, sort_keys=True))

def _valid_proof(prev_proof, proof):
    guess = _sha(str(prev_proof + proof))
    return guess[:DIFFICULTY] == PROBLEM * DIFFICULTY

def _pow(last_proof):
    while not _valid_proof(last_proof, proof:=random.randrange(-100_0000, 100_0001)):
        continue
    return proof

def _valid_chain(chain):
    return all(_hash(prev_block) == block['previous_hash']
               for prev_block, block in zip(chain, chain[1:]))


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        self.new_block(previous_hash=1, proof=100)

    @property
    def last_block(self):
        return self.chain[-1]
    
    def __len__(self):
        return len(self.chain)
    
    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append(
            dict(sender=sender, recipient=recipient, amount=amount, timestamp=time.time()))
        return self.last_block['index'] + 1
    
    def new_block(self, proof, previous_hash=None):
        block = dict(index=len(self) + 1,                       # 1, 2, 3, ...
                     timestamp=time.time(),
                     transactions=self.current_transactions,
                     nonce=proof,
                     previous_hash=previous_hash or _hash(self.last_block))
        self.chain.append(block)
        self.current_transactions = []
        return block
    
    def register_node(self, address):
        url = urlparse(address)         # scheme='http', netloc='127.0.0.1:5000', path='/chain...'
        self.nodes.add(url.netloc)      # '127.0.0.1:5000'

    def resolve_conflicts(self):
        new_chain = None
        my_length = len(self)
        for node in self.nodes:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                chain = response.json()['chain']
                if (length := len(chain)) > my_length and _valid_chain(chain):
                    my_length, new_chain = length, chain
        if new_chain is not None:
            self.chain = new_chain
            return True
        return False
    

blockchain = Blockchain()
headers = {'Content-Type': 'application/json; charset=utf-8'}
app = Flask(__name__)

@app.route('/chain', methods=['GET'])
def full_chain():
    print('\nchain info requested!')
    response = dict(chain=blockchain.chain)     #, length=len(blockchain))
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

    if 'type' not in values:
        values['type'] = 'sharing'
        for node in blockchain.nodes:
            requests.post(f'http://{node}/transactions/new', headers=headers, data=json.dumps(values))
            print('share transaction to >>', f'http://{node}')
    return jsonify(response), 201


@app.route('/mine', methods=['GET'])
def mine():
    print('\nMINING STARTED')
    last_proof = blockchain.last_block['nonce']
    proof = _pow(last_proof)

    blockchain.new_transaction(sender=mine_owner, recipient=node_identifier, amount=mine_profit)
    block = blockchain.new_block(proof)
    print('MINING FINISHED')

    response = dict(message='new block found', 
                    index=block['index'],
                    transactions=block['transactions'],
                    nonce=block['nonce'],
                    previous_hash=block['previous_hash'])
    for node in blockchain.nodes:
        data = dict(miner_node=f'http://{mynode}', new_nonce=proof)
        alarm_res = requests.get(f'http://{node}/nodes/resolve', headers=headers, data=json.dumps(data))
        if 'ERROR' not in alarm_res.text:
            response = dict(message='new block completed',
                            index=block['index'],
                            transactions=block['transactions'],
                            nonce=block['nonce'],
                            previous_hash=block['previous_hash'])
        else:
            block = blockchain.new_block(proof)
    return jsonify(response), 200


@app.route('/nodes/resolve', methods=['GET'])
def resolve():
    request_node_info = request.get_json()
    required = ['miner_node', 'new_nonce']
    if not all(k in request_node_info for k in required):
        return 'missing values', 400
    
    my_previous_hash = blockchain.last_block['previous_hash']
    last_proof = blockchain.last_block['nonce']
    miner_chain_info = requests.get(request_node_info['miner_node'] + '/chain', headers=headers)
    print('다른 노드에서 요청 온 블록, 검증 시작')
    new_block_previous_hash = json.loads(miner_chain_info.text)['chain'][-2]['previous_hash']
    if (my_previous_hash == new_block_previous_hash and
        _valid_proof(last_proof, int(request_node_info['new_nonce']))):
        print('다른 노드에서 요청 온 블록, 검증결과 정상!!!')
        replaced = blockchain.resolve_conflicts()
        if replaced:
            print('Replaced length:', len(blockchain))
            response = dict(message=f'Our chain was replaced >> {mynode}',
                            new_chain=blockchain.chain)
        else:
            response = dict(message='Our chain is authoritative', chain=blockchain.chain)
    else:
        print('다른 노드에서 요청 온 블록, 검증결과 이상 발생!!!!!')
        response = dict(message=f'Our chain is authoritative >> {mynode}',
                        chain=blockchain.chain)
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_node():
    v = request.get_json()
    print('\nRegister nodes!', v)
    if (new_node := v.get('nodes')) is None:
        return 'Error: Please supply a valid list of nodes', 400
    if new_node.split('//')[1] in blockchain.nodes:
        print('Node already registered')
        response = dict(message='Already registered node', total_nodes=list(blockchain.nodes))
    else:
        # 내 노드에 new_node 등록
        blockchain.register_node(new_node)
        
        # new_node에 내 노드 등록
        data = dict(nodes=f'http://{mynode}')
        print('My Node Info', data['nodes'])
        requests.post(new_node + '/nodes/register', headers=headers, data=json.dumps(data))

        # 내 타 노드에 new_node 등록
        for add_node in blockchain.nodes:
            add_node = 'http://' + add_node
            if add_node != new_node:
                print('add_node:', add_node)
                data = dict(nodes=new_node)
                requests.post(add_node + '/nodes/register', headers=headers, data=json.dumps(data))
        
        response = dict(message='New nodes have been added', total_nodes=list(blockchain.nodes))
    return jsonify(response), 201


app.run(host=myip, port=myport)