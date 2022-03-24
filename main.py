from fastapi import FastAPI, HTTPException

import blockchain


app = FastAPI()

bc = blockchain.Blockchain()


# mine a block
@app.post('/mine_block')
def mine_block(data: str):
    if not bc.is_chain_valid():
        return HTTPException(
            status_code=400, 
            detail='Blockchain is invalid')
    else:
        block = bc.mine_block(data=data)
        return block

# return the whole blockchain
@app.get('/blockchain')
def get_blockchain():
    if not bc.is_chain_valid():
        return HTTPException(
            status_code=400, 
            detail='Blockchain is invalid')
    else:
        chain = bc.chain
        return chain


# return previous block
@app.get('/previous_block')
def get_previous_block():
    if not bc.is_chain_valid():
        return HTTPException(
            status_code=400, 
            detail='Blockchain is invalid')
    else:
        return bc.get_previous_block()


@app.get('/validate')
def is_valid():
    return bc.is_chain_valid()