from hashlib import sha256
import time
import json

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, local_accuracy, model_params):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.local_accuracy = local_accuracy
        self.model_params = model_params
        
    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
    
class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.generate_genesis_block()
        self.pow_difficulty = 2
        
    def generate_genesis_block(self):
        genesis_block = Block(index=0, transactions=None, timestamp=time.time(), previous_hash="0", local_accuracy=0, model_params=None)
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
        
    @property
    def last_block(self):
        return self.chain[-1]
    
    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        
        if previous_hash != block.previous_hash:
            return False
        
        if not self.is_valid_proof(block, proof):
            return False
        
        block.hash = proof
        self.chain.append(block)
        return True
    
    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * self.pow_difficulty) and block_hash == block.compute_hash())
    
    def proof_of_work(self, block):
        block.nonce = 0
        
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * self.pow_difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash
        
    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        if not self.unconfirmed_transactions:
            return False
        
        last_block = self.last_block
        
        new_block = Block(index=last_block.index + 1, transactions=self.unconfirmed_transactions, 
                          timestamp=time.time(), previous_hash=last_block.hash, local_accuracy=0, model_params=None)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index

    def check_chain_validity(self, chain):
        result = True
        previous_hash = "0"
        
        # Iterate through every block
        for block in chain:
            block_hash = block.hash
            
            # Remove the hash field to recompute the hash again
            # using `compute_hash` method.
            delattr(block, "hash")
            
            if not self.is_valid_proof(block, block_hash) or previous_hash != block.previous_hash:
                result = False
                break
            
            block.hash, previous_hash = block_hash, block_hash
        return result
    
    
    