import requests
from web3 import Web3
import json

# Initialize Web3
#alchemy_url = add ur url
web3 = Web3(Web3.HTTPProvider(alchemy_url))

# Verify connection
if not web3.isConnected():
    print("Failed to connect to the Polygon network")
else:
    print("Connected to the Polygon network")

# Contract addresses and ABI for USDC and USDC.e on Polygon
contract_addresses = {
    'USDC': '0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359',
    'USDC2': '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'  # Assume this is USDC.e
}
abi = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
]

# Initialize contracts
usdc_e_contract = web3.eth.contract(address=contract_addresses['USDC2'], abi=abi)

# Target address to check senders to
target_address = '0xa26e73C8E9507D50bF808B7A2CA9D5dE4fcC4A04'

def fetch_transactions(contract_address):
    all_transactions = []
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
        print(response.json())
        if response.status_code == 200:
            result = response.json().get('result', {})
            transactions = result.get('transfers', [])
            all_transactions.extend(transactions)
            page_key = result.get('pageKey')
            if not page_key:  # Break the loop if no more pageKey is provided
                break
        else:
            print(f"Failed to fetch transactions: {response.text}")
            break
    return all_transactions

# Collect all transactions
transactions_usdc = fetch_transactions(contract_addresses['USDC'])
transactions_usdc_e = fetch_transactions(contract_addresses['USDC2'])

# Combine transactions from both USDC and USDC.e
transactions = transactions_usdc + transactions_usdc_e

# Store unique sender addresses
senders = set(tx['from'] for tx in transactions)

# Map to store balances
non_zero_balances = {}

# Check USDC.e balances and store non-zero balances
for sender in senders:
    address = Web3.to_checksum_address(sender)
    balance = usdc_e_contract.functions.balanceOf(address).call()
    if balance > 0:
        non_zero_balances[address] = balance
        print(f"Address: {sender}, USDC.e Balance: {balance}")

# Save non-zero balances to a JSON file
with open('non_zero_balances.json', 'w') as file:
    json.dump(non_zero_balances, file, indent=4)

print("Saved non-zero balances to 'non_zero_balances.json'.")
