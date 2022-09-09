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
- Improve error handling

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

Docker

Build the image
```
docker image build -t flask_docker .
```

Run 
```
docker run -p 5000:5000 -d flask_docker
```

## Usage
- Navigate to /generate and enter a password to generate key pairs
--  First key created on the chain receives "100" coins.

- On the /transactions page, enter the same password, a recipient address and an amount 
to transfer some coins to another address.
- Navigate to /chain to look view the transaction.
- You can also go to /balance to look up the balances of a public key.
### Generate
Enter a password to generate public and private key to be used.
".pem" file containing encrypted private key will be generated onto the local directory.
### Transaction
Transfer "coins" to a recipient's public key
The transaction will still be created regardless of wrong password or not having the enough amount. It will just not be added onto the chain.
### Chain
View all blocks that are added onto the chain.
### Balance
Returns balance of a specific public key.










