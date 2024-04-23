from solana.rpc.api import Client
from solana.publickey import PublicKey

# Initialize the Solana client
# You can use a specific Solana RPC endpoint URL (e.g., mainnet-beta) for better performance
solana_client = Client(os.getenv("SOLANA_RPC_ENDPOINT_URL"))

# Specify the wallet public key
wallet_public_key = PublicKey(os.getenv("PUBLIC_KEY"))
def get_account_balance():
    pass
# Get the token account balances for the wallet
    response = solana_client.get_token_accounts_by_owner(wallet_public_key, {"program_id": PublicKey(os.getenv("INPUT_MINT"))})
    token_amount=0
# Iterate through token accounts and print balances
    for account in response['result']['value']:
        account_info = account['account']['data']['parsed']['info']
        mint_address = account_info['mint']
        token_amount = account_info['tokenAmount']['uiAmount']  # The token amount
        decimals = account_info['tokenAmount']['decimals']  # The number of decimals for the token

        print(f"Mint Address: {mint_address}")
        print(f"Balance: {token_amount} (Decimals: {decimals})")
    return token_amount

# You can adjust the endpoint URL and the public key as per your requirements.
