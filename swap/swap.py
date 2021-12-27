from web3 import Web3
import json
from configparser import ConfigParser
import datetime
import sys
from ftm_addresses import token_abi, pairs_abi, router_abi, factory_abi, ftm_provider
from ftm_addresses import factory_addresses, router_addresses
from ftm_addresses import token_address_dict, pair_address_dict
import math
from datetime import datetime
import calendar
import time

class Swap:

    def swap(self, wallet_address,amount, input, output):
        web3 = Web3(Web3.HTTPProvider(ftm_provider))
        wallet_address = web3.toChecksumAddress(wallet_address)
        token_address_in = web3.toChecksumAddress(token_address_dict[input])
        #dex = 'sushi'
        dex = 'spooky'
        token_address_out = web3.toChecksumAddress(token_address_dict[output])
        tokens_bought, tx = self.buy(web3, 
                            token_address_in = token_address_in, 
                            token_address_out = token_address_out, 
                            thisdex = dex, 
                            wallet_address = wallet_address, 
                            spend_amount=amount
                            )


    def buy(self, web3, token_address_in, token_address_out, thisdex, wallet_address, holy_key,
            spend_amount, slippage=0.05, dt=20, max_gas = 323186, gas_price = 120):
        d = datetime.utcnow()
        unixtime = calendar.timegm(d.utctimetuple())
        deadline = unixtime + dt * 1000
        amount_in = web3.toWei(str(spend_amount), 'Ether')
        token_contract_in = web3.eth.contract(address=web3.toChecksumAddress(token_address_in), abi=token_abi)
        token_balance_in = token_contract_in.functions.balanceOf(wallet_address).call()
        if token_balance_in < amount_in:
            print("Insufficient balance, transaction will fail")
        router_address = router_addresses[thisdex]
        router_contract = web3.eth.contract(address=web3.toChecksumAddress(router_address), abi=router_abi)
        token_amount_out = router_contract.functions.getAmountsOut(amount_in, [token_address_in, token_address_out]).call()
        decimal = token_contract_in.functions.decimals().call()
        print("Expected out: {}".format(token_amount_out[1] / 10**decimal))
        min_amount_out = int(token_amount_out[1] * (1.0 - slippage))
        time.sleep(1)
        buy_tx = router_contract.functions.swapExactTokensForTokens(
            amount_in,
            min_amount_out,
            [web3.toChecksumAddress(token_address_in),
            web3.toChecksumAddress(token_address_out)],
            wallet_address,
            deadline).buildTransaction({
            'gas': max_gas,
            'gasPrice': web3.toWei(gas_price, 'gwei'),
            'nonce': web3.eth.get_transaction_count(wallet_address),
        })
        signed_tx = web3.eth.account.sign_transaction(buy_tx, holy_key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return min_amount_out, tx_hash

