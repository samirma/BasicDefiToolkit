from web3 import Web3
import json
from configparser import ConfigParser
import datetime
from transaction_manager import * 
from ftm_addresses import token_abi, pairs_abi, router_abi, factory_abi, ftm_provider
from ftm_addresses import factory_addresses, router_addresses
from ftm_addresses import token_address_dict, pair_address_dict
import math
from datetime import datetime
import calendar
import time


class Swap:

    def __init__(self, txManager):
        web3 = Web3(Web3.HTTPProvider(ftm_provider))
        self.web3 = web3,
        self.txManager:TransactionManager = txManager

    def swap(self, wallet_address, amount, input, output, key):
        web3 = self.web3
        token_address_in = token_address_dict[input]
        #dex = 'sushi'
        dex = 'spooky'
        token_address_out = token_address_dict[output]
        self.buy(web3, 
                token_address_in = token_address_in, 
                token_address_out = token_address_out, 
                thisdex = dex, 
                wallet_address = wallet_address, 
                spend_amount=amount,
                holy_key=key
                )

    def buy(self, web3, token_address_in, token_address_out, thisdex, wallet_address, holy_key,
            spend_amount, slippage=0.05, dt=20):
        d = datetime.utcnow()
        unixtime = calendar.timegm(d.utctimetuple())
        deadline = unixtime + dt * 1000
        #amount_in = self.convertToSwap(spend_amount)
        amount_in = spend_amount

        token_contract_checked = web3.toChecksumAddress(token_address_in)

        token_contract_in = web3.eth.contract(address=token_contract_checked, abi=token_abi)
        token_balance_in = token_contract_in.functions.balanceOf(wallet_address).call()
        #if token_balance_in < amount_in:
        #    print(f"Insufficient balance, transaction will fail token_balance: {token_balance_in} amount_in: {amount_in}")
            #exit(0)
        
        router_address = router_addresses[thisdex]
        router_contract = web3.eth.contract(address=web3.toChecksumAddress(router_address), abi=router_abi)
        token_amount_out = router_contract.functions.getAmountsOut(amount_in, [token_address_in, token_address_out]).call()

        min_amount_out = int(token_amount_out[1] * (1.0 - slippage))
        
        funSwap = router_contract.functions.swapExactTokensForTokens(
            amount_in,
            min_amount_out,
            [web3.toChecksumAddress(token_address_in),
            web3.toChecksumAddress(token_address_out)],
            wallet_address,
            deadline
        )

        self.txManager.execute_transation(
            funTx=funSwap,
            web3 = web3,
            wallet_address = wallet_address,
            key = holy_key
        )

    def get_balance(self, coin_name, wallet_address):
        web3 = self.web3
        token_address_in = token_address_dict[coin_name]
        token_contract_checked = web3.toChecksumAddress(token_address_in)
        wallet_address_checked = web3.toChecksumAddress(wallet_address)
        return self.get_balance_by_checked_address(token_address = token_contract_checked, wallet_address = wallet_address_checked) 
        
    def get_balance_by_checked_address(self, token_address, wallet_address):
        web3 = self.web3
        token_contract_in = web3.eth.contract(address=token_address, abi=token_abi)
        return token_contract_in.functions.balanceOf(wallet_address).call()

    def convertToSwap(self, spend_amount):
        return self.web3.toWei(str(spend_amount), 'Ether')

    def decimal_value(self, token_address):
        return self.decimal_value_by_checked_address(self.web3.toChecksumAddress(token_address))

    def decimal_value_by_checked_address(self, token_address):
        token_contract = self.web3.eth.contract(address=token_address, abi=token_abi)
        return token_contract.functions.decimals().call()

    def convert_amount_to_swap(self, amount, token_address):
        symbolDecimals = self.decimal_value(token_address)
        return amount * 10 ** symbolDecimals


    def convert_amount_to_human(self, amount, token_address):
        symbolDecimals = self.decimal_value(token_address)
        return amount / 10 ** symbolDecimals

    def approve_spend(self, token_address_in, router_address, wallet_address, key, total_max_spend=1.0):
        web3 = self.web3
        cs_router_address = web3.toChecksumAddress(router_address)
        cs_wallet_address = web3.toChecksumAddress(wallet_address)
        token_contract_in = web3.eth.contract(address=web3.toChecksumAddress(token_address_in), abi=token_abi)
        allowed = int(token_contract_in.functions.allowance(cs_wallet_address, cs_router_address).call())
        print("Approved up to {}".format(allowed))
        max_amount = int(web3.toWei(total_max_spend, 'ether'))
        if allowed < max_amount:
            self.txManager.execute_transation
        else:
            tx = 'approval exists'
        allowed = token_contract_in.functions.allowance(cs_wallet_address, cs_router_address).call()
        return(allowed, tx)

