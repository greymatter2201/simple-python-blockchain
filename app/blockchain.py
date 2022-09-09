import time
from .keygen import Keys

keys = Keys()


class Blockchain:


    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.difficulty = 4
        self.prefix = '0' * self.difficulty
        self.global_balances = {}
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = self.new_block(previous_hash=1)
        self._mine(genesis_block)

    def new_transactions(self, password, recipient, amount):
        try:
            private_key = keys.load_pem_private(password)
        except ValueError:
            return False

        public_key = keys.gen_pub_key(private_key, True)
        sender = public_key.splitlines()[1].decode()
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': int(amount)
        }
        transaction_hash = keys.SHA256(transaction)
        signature = keys.signMessage(private_key, transaction_hash.encode())
        self.current_transactions.append((signature.hex(), transaction_hash, transaction))

        return True

    def new_block(self, previous_hash=None):
        # Creates a new block
        block = {
            'block_index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'nonce': 1,
            'previous_blockhash': previous_hash
        }
        return block

    def generate_keys(self, password):
        public_key = keys.gen_key_pem(password)
        if not self.global_balances:
            key = public_key.splitlines()[1].decode()
            self.global_balances[key] = 100
        return public_key

    def _mine(self, block):
        # Finds a nonce such that the resulting hash
        # starts with the prefix
        # When found, the block is appended to the chain
        self._validate_transactions()
        while not keys.SHA256(block).startswith(self.prefix):
            block['nonce'] += 1
        block_hash = keys.SHA256(block)
        self.chain.append((block_hash, block))
        self.current_transactions = []

    def _validate_transactions(self):
        begin = "-----BEGIN PUBLIC KEY-----\n"
        end = "\n-----END PUBLIC KEY-----\n"
        for index, transaction in enumerate(self.current_transactions):
            signature, message = transaction[0], transaction[1]
            public_pem = transaction[2]['sender'].join([begin, end])
            public_key = keys.load_pem_public(public_pem.encode())
            verified = keys.verify(public_key, message.encode(), bytes.fromhex(signature))

            transferred = self._update_balance(transaction)

            if not verified or not transferred:
                del self.current_transactions[index]

    def _update_balance(self, transaction):
        sender, recipient = transaction[2]['sender'], transaction[2]['recipient']
        amount = transaction[2]['amount']
        try:
            enough = self.global_balances[sender] >= amount
        except KeyError:
            return False
        else:
            if not enough:
                return False

            if recipient not in self.global_balances:
                self.global_balances[recipient] = 0

            self.global_balances[recipient] += amount
            self.global_balances[sender] -= amount
            return True

    def mine(self):
        previous_hash = self.chain[-1][0]
        self._mine(self.new_block(previous_hash))

    def check_valid_chain(self):
        # Going through the chain
        # To check if previous_hash in the current block,
        # is equal to the hash of the previous block
        # Gensis block is ignored
        for i in reversed(range(1,len(self.chain))):
            previous_hash = self.chain[i][1]['previous_blockhash']
            previous_block = self.chain[i-1][0]
            print(previous_hash, previous_block)
            if previous_block != previous_hash:
                return False
        return True