import base58
import base64
import json

from solders import message
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction

from solana.rpc.types import TxOpts
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Processed

from jupiter_python_sdk.jupiter import Jupiter, Jupiter_DCA
import sys
import os
from solana_api.main import get_account_balance
# Add the directory containing jupiter_api.py to sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
package_dir = os.path.join(script_dir, 'jupiter_api_base')
sys.path.append(package_dir)

private_key = Keypair.from_bytes(base58.b58decode(os.getenv("PRIVATE_KEY"))) # Replace PRIVATE-KEY with your private key as string
async_client = AsyncClient(os.getenv("SOLANA_RPC_ENDPOINT_URL")) # Replace SOLANA-RPC-ENDPOINT-URL with your Solana RPC Endpoint URL
jupiter = Jupiter(
    async_client=async_client,
    keypair=private_key,
    quote_api_url="https://quote-api.jup.ag/v6/quote?",
    swap_api_url="https://quote-api.jup.ag/v6/swap",
    open_order_api_url="https://jup.ag/api/limit/v1/createOrder",
    cancel_orders_api_url="https://jup.ag/api/limit/v1/cancelOrders",
    query_open_orders_api_url="https://jup.ag/api/limit/v1/openOrders?wallet=",
    query_order_history_api_url="https://jup.ag/api/limit/v1/orderHistory",
    query_trade_history_api_url="https://jup.ag/api/limit/v1/tradeHistory"
)



"""
OPEN LIMIT ORDER
"""
async def buy_order(input_mint, out_mint,amount):
  token_amount=await get_account_balance(input_mint)
  if token_amount<amount:
    print("Insufficient token balance")
    return "Insufficient token balance"
  transaction_data = await jupiter.open_order(
        input_mint=input_mint,
        output_mint=out_mint,
        in_amount=amount,
        out_amount=0,
    )
    # Returns dict: {'transaction_data': serialized transactions to create the limit order, 'signature2': signature of the account that will be opened}

  raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(transaction_data['transaction_data']))
  signature = private_key.sign_message(message.to_bytes_versioned(raw_transaction.message))
  signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature, transaction_data['signature2']])
  opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
  result = await async_client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)
  transaction_id = json.loads(result.to_json())['result']
  explorer_url=f"https://explorer.solana.com/tx/{transaction_id}"
  print(f"Transaction sent: {explorer_url}")
  return transaction_id



