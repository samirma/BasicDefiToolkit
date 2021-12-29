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

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


class Swap:

    def __init__(self):
        web3 = Web3(Web3.HTTPProvider(ftm_provider))
        self.web3 = web3

    def swap(self, wallet_address, amount, input, output, key):
        web3 = self.web3
        wallet_address = web3.toChecksumAddress(wallet_address)
        token_address_in = token_address_dict[input]
        #dex = 'sushi'
        dex = 'spooky'
        token_address_out = token_address_dict[output]
        tokens_bought, tx = self.buy(web3, 
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
        if token_balance_in < amount_in:
            print(f"Insufficient balance, transaction will fail token_balance: {token_balance_in} amount_in: {amount_in}")
            #exit(0)
        router_address = router_addresses[thisdex]
        router_contract = web3.eth.contract(address=web3.toChecksumAddress(router_address), abi=router_abi)
        token_amount_out = router_contract.functions.getAmountsOut(amount_in, [token_address_in, token_address_out]).call()
        decimal = token_contract_in.functions.decimals().call()
        print("Expected out: {}".format(token_amount_out[1] / 10**decimal))
        min_amount_out = int(token_amount_out[1] * (1.0 - slippage))
        time.sleep(1)

        trans = {
            'gas': web3.eth.getBlock("latest").gasLimit,
            'gasPrice': 211348,#web3.eth.gasPrice,
            'nonce': web3.eth.get_transaction_count(wallet_address),
        }

        print(f"Trnsaction: {trans}")

        buy_tx = router_contract.functions.swapExactTokensForTokens(
            amount_in,
            min_amount_out,
            [web3.toChecksumAddress(token_address_in),
            web3.toChecksumAddress(token_address_out)],
            wallet_address,
            deadline).buildTransaction(trans)
        signed_tx = web3.eth.account.sign_transaction(buy_tx, holy_key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        hashes = Web3.toHex(tx_hash)
        time.sleep(8)
        status = web3.eth.get_transaction_receipt(hashes)
        txStatus = status.status
        if int(txStatus) == 1:
            print(style.YELLOW+"SuccessFully Bought $symbol at transactionHash {}".format(hashes)+style.RESET)
        else:
            print(style.MAGENTA+"TRANSACTION FAILED !!"+style.RESET)

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

