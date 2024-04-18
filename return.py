import requests
import json
from web3 import Web3

# Initialize Web3
#alchemy_url = add ur url
web3 = Web3(Web3.HTTPProvider(alchemy_url))

# Verify connection
if not web3.isConnected():
    print("Failed to connect to the Polygon network")
else:
    print("Connected to the Polygon network")

# Function to get the nonce for a given address
def get_nonce(address):
    return web3.eth.getTransactionCount(Web3.toChecksumAddress(address))

# Function to fetch incoming USDC.e transactions to a given address using Alchemy API
def fetch_incoming_transactions(alchemy_url, contract_address, target_address):
    transactions = []
    page_key = None
    while True:
        params = {
            "fromBlock": "0x0",
            "toBlock": "latest",
            "toAddress": target_address,
            "contractAddresses": [contract_address],
            "withMetadata": False,
            "excludeZeroValue": True,
            "category": ["erc20"],
            "maxCount": "0x3e8"  # 1000 in hexadecimal
        }
        if page_key:
            params["pageKey"] = page_key

        payload = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "alchemy_getAssetTransfers",
            "params": [params]
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        response = requests.post(alchemy_url, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json().get('result', {})
            transactions.extend(result.get('transfers', []))
            page_key = result.get('pageKey')
            if not page_key:  # Break the loop if no more pageKey is provided
                break
        else:
            break

    return transactions

# Load the non_zero_balances data
with open('non_zero_balances.json', 'r') as file:
    non_zero_balances = json.load(file)

# Alchemy URL and USDC.e contract address
usdc_e_contract_address = '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'  # USDC.e contract address on Polygon

# Prepare unsigned transactions
unsigned_transactions = []
for address, balance in non_zero_balances.items():
    transactions = fetch_incoming_transactions(alchemy_url, usdc_e_contract_address, address)
    if transactions:
        # We assume the most recent sender is the depositor
        last_sender = transactions[-1]['from']
        nonce = get_nonce(address)  # Fetch the nonce for the address

        # Create unsigned transaction data
        data = f"0xa9059cbb{last_sender[2:].zfill(64)}{hex(balance)[2:].zfill(64)}"
        transaction = {
            'from': address,
            'to': last_sender,
            'value': '0x0',
            'gas': '0xea60',  # 60000 in hexadecimal
            'gasPrice': '0x4a817c800',  # 20 Gwei in hexadecimal
            'nonce': hex(nonce),  # This needs to be set according to the account nonce
            'data': data
        }
        unsigned_transactions.append(transaction)

# Save unsigned transactions to a JSON file
with open('unsigned_transactions.json', 'w') as file:
    json.dump(unsigned_transactions, file, indent=4)

print("Unsigned transactions saved to 'unsigned_transactions.json'.")
