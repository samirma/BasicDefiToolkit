from web3 import Web3
import json
from configparser import ConfigParser
import datetime
from swap.swap import *
from ftm_addresses import token_address_dict, token_abi, hector_abi, hector_contract_address
from web3.gas_strategies.time_based import medium_gas_price_strategy


class ProfileExecutor:

    def __init__(self, txManager, origin_address, dest_address, transaction_address, swap):
        self.txManager:TransactionManager = txManager
        self.origin_address = origin_address
        self.dest_address = dest_address
        self.transaction_address = transaction_address
        self.swap: Swap = swap
    
    def execute_profit(self, web3):
        total_fees = self.txManager.get_total_fees(self, web3)
        avarage_fee = total_fees / len(self.transactions)

        balance = self.swap.get_balance_by_address(
            token_address_in=self.origin_address,
            wallet_address=self.swap.wallet_address
        )

        human_balance = self.swap.convert_amount_to_human(balance, self.origin_address)

        self.swap.swap(
            amount=human_balance,
            input=self.origin_address,
            output=self.dest_address
        )

        
