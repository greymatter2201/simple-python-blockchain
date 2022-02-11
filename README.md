# Simple (naive?) Python Blockchain with flask
## 
## Features
- Key Signing/Verification
- Public/Private Key Generation
- Check Balances
- Check if current chain is valid

## To-do
- Longest Chain Consensus 
- Proof of Work (Currently, blocks are added onto the chain with PoW but no ability to validate the work yet)
- Ability to add other nodes (P2P)

## Installation

Install the dependencies

```sh
cd simple-python-blockchain
pipenv install 
```

Activate the enviornment and run the script

```sh
pipenv shell
export FLASK_APP=web.py
flask run 
```
By default flask will run on //localhost:5000




