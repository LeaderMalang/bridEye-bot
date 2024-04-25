from solathon import AsyncClient, Transaction, PublicKey, Keypair,Client
import os
import asyncio
# Initialize the Solana client
# You can use a specific Solana RPC endpoint URL (e.g., mainnet-beta) for better performance
solana_client = AsyncClient(os.getenv("SOLANA_RPC_ENDPOINT_URL"))
# program_id =os.getenv("INPUT_MINT")
# Specify the wallet public key
wallet_public_key = PublicKey(os.getenv("PUBLIC_KEY"))
async def get_account_balance(program_id):
    
# Get the token account balances for the wallet
    response = await solana_client.get_token_accounts_by_owner(wallet_public_key,program_id=program_id)
    token_amount=0
    if "error" in response:
        msg=response['error']['message']
        print(msg)
        return token_amount
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


#balance=get_account_balance()

# asyncio.run(get_account_balance())
