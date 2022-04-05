from hashlib import sha256
import json
import time
from fastapi import FastAPI
from pydantic import BaseModel


# Create a block that stores the data in json formate
# Encode the data and encrypt it using SHA256 algorithm

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = None

    def ComputeHash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()  # what is json.encode() method doing?


# Creating a chain of blocks

class BlockChain:
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()
        self.difficulty = 2

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.ComputeHash()  # Creating a new hash attribute for the genesis block object
        self.chain.append(genesis_block)  # making a chain of blocks

    @property  # Unserstand the property decorator properly?
    def last_block(self):
        return self.chain[-1]

    # The Proof of Work ensures that generating the hash for each block is a difficult process

    def ProofOfWork(self, block):
        computed_hash = block.ComputeHash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.ComputeHash()
        return computed_hash

    def AddBlock(self, block, proof):
        # previous_hash = self.last_block.hash
        # if previous_hash != block.previous_hash:
        #     return False
        # if not self.IsValidProof(block, proof):
        #     return False
        block.hash = proof
        self.chain.append(block)
        return True

    # def IsValidProof(self, block, block_hash):
    #     return block_hash.startswith('0' * self.difficulty) and block_hash == block.ComputeHash()

    def AddNewTransaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    # Mining is the process of adding a new block to the chain and performing all the assosiated computation

    def Mine(self):
        if not self.unconfirmed_transactions:
            return False
        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)
        proof = self.ProofOfWork(new_block)
        self.AddBlock(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index


# Add another block to the blockchain

chain = BlockChain()

chain.AddNewTransaction({"Rakshit2Kishan": 45,
                         "Shalina2Kishan": 90,
                         "Kishan2Rakshit": 100})
chain.Mine()

chain.AddNewTransaction({"Rakshit2Shalina": 45,
                         "Shalina2Kishan": 90,
                         "Kishan2Shalina": 100})
chain.Mine()

# Print the various blocks of the blockchain

# for obj in chain.chain:
#     print(obj.__dict__)

# Write a web API using Fast API

BlockchainApp = FastAPI()


# Get Greetings
@BlockchainApp.get("/myblockchain/welcome")
def read_root():
    return "greetings!, welcome to my blockchain"


# Post transactions on the blockchain
@BlockchainApp.post("/myblockchain/{transaction}")
def add_transactions(transaction: str):
    chain.AddNewTransaction(transaction)
    chain.Mine()
    return "The transaction is successfully added to the chain"


# Get the current state of blockchain
@BlockchainApp.get("/myblockchain/chain")
def get_blockchain():
    return [obj.__dict__ for obj in chain.chain]


# Trying to inject fault in the blockchain externally
chain.chain[1].transactions = "Fraud transaction"

# for obj in chain.chain:
#     print(obj.__dict__)  # This blockchain is not robust to fradulent injects
