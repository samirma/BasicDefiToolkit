from web3 import Web3
import json
from configparser import ConfigParser
import datetime
from swap.swap import *
from ftm_addresses import token_address_dict, token_abi, hector_abi, hector_contract_address
from web3.gas_strategies.time_based import medium_gas_price_strategy
from config import *

class ProfileExecutor:

    def __init__(self, txManager, origin_address, dest_address, transaction_address, swap):
        self.txManager:TransactionManager = txManager
        self.origin_address = origin_address
        self.dest_address = dest_address
        self.transaction_address = transaction_address
        self.swap: Swap = swap
        self.transactions = []
    
    def execute_profit(self, web3):
        total_fees = self.txManager.get_total_fees(web3)

        avarage_fee = 0
        transactions_cpunt = len(self.transactions)
        if (transactions_cpunt > 0):
            avarage_fee = total_fees / transactions_cpunt

        balance = self.swap.get_balance_by_address(
            token_address_in=self.origin_address,
            wallet_address=self.swap.wallet_address
        )

        human_balance = self.swap.convert_amount_to_human(balance, self.origin_address)

        print(f"Swap {human_balance} from {self.origin_address} to {self.dest_address}")

        #return 
        self.swap.swap(
            amount=human_balance,
            input=self.origin_address,
            output=self.dest_address
        )


if __name__ == "__main__":

    web3 = Web3(Web3.HTTPProvider(ftm_provider))

    config_object:Config = get_config()

    txManager = TransactionManager(
        key = config_object.fantom_key,
        wallet_address = config_object.wallet
    )

    swap: Swap = Swap(
        txManager=txManager,
        wallet_address = config_object.wallet
    )
    
    profileExecutor = ProfileExecutor(
        txManager = txManager,
        origin_address=token_address_dict['HEC'],
        dest_address=token_address_dict['DAI'],
        transaction_address=token_address_dict['FTM'],
        swap = swap
    )

    profileExecutor.execute_profit(web3)


        
