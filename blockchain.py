"""
Basic Overview of a Blockchain

Genesis Block
{
    index: 0,
    timestamp: current time,
    data: 'the first block',
    proof: 3,
    previous_hash: '0'
}
   -> hash() -> abcdef

{
    index: 1,
    timestamp: current time,
    data: 'hello world',
    proof: 123,
    previous_hash: 'abcdef',
}
    -> hash() -> ghijkl

{
    index: 2,
    timestamp: current time,
    data: 'hello world again',
    proof: 789,
    previous_hash: 'ghijkl',
}
"""

import datetime as dt
import hashlib
import json


class Blockchain:
    
    def __init__(self):
        self.chain = list()
        genesis_block = self.create_block(
            data='The first block', proof=1, previous_hash='0', index=1)
        self.chain.append(genesis_block)

    def mine_block(self, data: str):
        previous_block = self.get_previous_block()
        previous_proof = previous_block["proof"]
        index = len(self.chain) + 1
        proof = self.proof_of_work(previous_proof, index, data)
        previous_hash = self._hash(block=previous_block)
        block = self.create_block(
            data=data, proof=proof, previous_hash=previous_hash, index=index)
        self.chain.append(block)
        return block
        
    def _hash(self, block: dict):
        """
        Hashes a block and returns the hash value of the block
        """
        encoded_block = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(encoded_block).hexdigest()

    def check_proof(self, new_proof: int, previous_proof: int, index: str, data: str):
        check = str(new_proof ** 2 - previous_proof ** 2 + index) + data

        return check.encode()

    def proof_of_work(self, previous_proof: str, index: int, data: str):
        new_proof = 1
        proof_checked = False

        while not proof_checked:
            print(new_proof)
            checked_proof = self.check_proof(
                new_proof=new_proof, 
                previous_proof=previous_proof, 
                index=index, 
                data=data)
            hash_value = hashlib.sha256(checked_proof).hexdigest()

            if hash_value[:4] == '0000':
                proof_checked = True
            else:
                new_proof += 1
            
        return new_proof

    def get_previous_block(self):
        return self.chain[-1]

    def create_block(self, data: str, proof: int, previous_hash: str, index: int):
        block = {
            "index": index,
            "timestamp" : str(dt.datetime.now()),
            "data": data,
            "proof": proof,
            "previous_hash": previous_hash
        }

        return block

    