from web3 import Web3
import json
from configparser import ConfigParser
import datetime
from transaction_manager import * 
from addresses.ftm_addresses import token_abi, pairs_abi, router_abi, factory_abi, ftm_provider
from addresses.ftm_addresses import factory_addresses, router_addresses
from addresses.ftm_addresses import token_address_dict, pair_address_dict
from time import sleep, time


class Swap:

    def __init__(self,
                txManager,
                wallet_address
            ):
        self.web3 = Web3(Web3.HTTPProvider(ftm_provider))
        self.txManager:TransactionManager = txManager
        self.wallet_address = wallet_address

    def swap(self,
            amount, 
            input, 
            output 
        ):
        web3 = self.web3
        #dex = 'sushi'
        dex = 'spooky'
        self.buy(web3, 
                token_address_in = input, 
                token_address_out = output, 
                thisdex = dex, 
                amount=amount
                )

    def buy(self, 
                web3, 
                token_address_in, 
                token_address_out, 
                thisdex,
                amount
                ):
                
        base = Web3.toChecksumAddress(token_address_in)
        DECIMALS = self.decimals(token_address_in)
        amount = int(amount * DECIMALS)

        router_address = router_addresses[thisdex]
        routerContract = web3.eth.contract(address=web3.toChecksumAddress(router_address), abi=router_abi)

        amount_out = routerContract.functions.getAmountsOut(amount, [base, Web3.toChecksumAddress(token_address_out)]).call()[-1]
        min_tokens = int(amount_out * (1 - (50 / 100)))

        funSwap = routerContract.functions.swapExactTokensForTokens(
            amount,
            min_tokens,
            [base, Web3.toChecksumAddress(token_address_out)],
            Web3.toChecksumAddress(self.wallet_address),
            deadline = int(time() + + 240)
        )

        self.txManager.execute_transation(
            funTx=funSwap,
            web3 = web3
        )

    def get_balance(self, coin_name, wallet_address):
        token_address_in = token_address_dict[coin_name]
        return self.get_balance_by_address(token_address = token_address_in, wallet_address = wallet_address) 
        
    def get_balance_by_address(self, token_address_in, wallet_address):
        web3 = self.web3
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
        DECIMALS = self.decimals(token_address)
        amount = amount * DECIMALS
        return amount

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

    def decimals(self, address):
        decimals = self.decimal_value(address)
        DECIMALS = 10 ** decimals
        return DECIMALS

        
