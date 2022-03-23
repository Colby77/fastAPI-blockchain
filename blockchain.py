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
        """
        Creates first block in blockchain (genesis block)
        and starts chain
        """
        self.chain = list()
        genesis_block = self.create_block(
            data='The first block', proof=1, previous_hash='0', index=1)
        self.chain.append(genesis_block)

    def mine_block(self, data: str):
        """
        Gets the previous block and proof

        Creates a new proof using previous proof, new index and data

        Hashes previous block and creates the new block with the previous 
        hash, data, proof and index

        Adds new block to the chain
        """
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
        """
        Checks a proof using mathematical formula in 'check'
        """
        check = str(new_proof ** 2 - previous_proof ** 2 + index) + data

        return check.encode()

    def proof_of_work(self, previous_proof: str, index: int, data: str):
        """
        Checks if the first 4 digits of a given hashed value is
        equal to '0000'

        Value starts at 1 and keeps going until the correct hashed value
        is found
        """
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
        """Returns last block in chain"""
        return self.chain[-1]

    def create_block(self, data: str, proof: int, previous_hash: str, index: int):
        """Creates new block"""

        block = {
            "index": index,
            "timestamp" : str(dt.datetime.now()),
            "data": data,
            "proof": proof,
            "previous_hash": previous_hash
        }

        return block

    def is_chain_valid(self):
        """
        Validates the block chain

        Starts at genesis block and for each block
        in chain, checks that:
            The next block's previous hash
            isn't the same as the current block's hash

            A hashed value using the current proof
            matches the hashed value of the next block in chain  
        """

        current_block = self.chain[0]
        block_index = 1

        while block_index < len(self.chain):
            next_block = self.chain[block_index]

            if next_block["previous_hash"] != self._hash(current_block):
                return False

            current_proof = current_block["proof"]
            next_index, next_data, next_proof = (
                next_block["index"],
                next_block["data"], 
                next_block["proof"]
                )
            hash_value = hashlib.sha256(self.check_proof(
                new_proof=next_proof,
                previous_proof=current_proof,
                index=next_index,
                data=next_data
            )).hexdigest()

            if hash_value[:4] != '0000':
                return False

            current_block = next_block
            block_index +=1

            return True
