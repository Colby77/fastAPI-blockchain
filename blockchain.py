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

    def create_block(self, data: str, proof: int, previous_hash: str, index: int):
        block = {
            "index": index,
            "timestamp" : str(dt.datetime.now()),
            "data": data,
            "proof": proof,
            "previous_hash": previous_hash
        }

        return block