from web3 import Web3
from ftm_addresses import token_abi, pairs_abi, router_abi, factory_abi
from ftm_addresses import factory_addresses, router_addresses
from ftm_addresses import token_address_dict, pair_address_dict

def approve_spend(web3, token_address_in, router_address, wallet_address, key, total_max_spend=1.0):
    
    cs_router_address = web3.toChecksumAddress(router_address)
    cs_wallet_address = web3.toChecksumAddress(wallet_address)
    token_contract_in = web3.eth.contract(address=web3.toChecksumAddress(token_address_in), abi=token_abi)
    allowed = int(token_contract_in.functions.allowance(cs_wallet_address, cs_router_address).call())
    print("Approved up to {}".format(allowed))
    max_amount = int(web3.toWei(total_max_spend, 'ether'))
    if allowed < max_amount:
        nonce = web3.eth.getTransactionCount(wallet_address)
        funTx = token_contract_in.functions.approve(cs_router_address, max_amount)
        tx = funTx.buildTransaction({
            'from': wallet_address,
            'gas': funTx.estimateGas(),
            'nonce': nonce,
            "gasPrice": web3.eth.gas_price
        })
        signed_tx = web3.eth.account.signTransaction(tx, key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx = web3.toHex(tx_hash)
    else:
        tx = 'approval exists'
    allowed = token_contract_in.functions.allowance(cs_wallet_address, cs_router_address).call()
    return(allowed, tx)

if __name__ == '__main__':
    web3 = Web3(Web3.HTTPProvider(endpoint))
    print("Operational?", web3.isConnected())
    token_symbol = 'BOO'
    wallet_address = web3.toChecksumAddress(wallet_address)
    this_dex = 'spooky'
    token_address = web3.toChecksumAddress(token_address_dict[token_symbol])
    approved_amt, tx = approve_spend(web3, token_address, this_dex, wallet_address, total_max_spend=1.0)
    print("amn: {} tx: {}".format(web3.fromWei(approved_amt, 'Ether'),tx))

