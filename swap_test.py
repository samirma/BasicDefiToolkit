from web3 import Web3
import json
from configparser import ConfigParser
import datetime
from swap.swap import *
from addresses.ftm_addresses import token_address_dict, token_abi, hector_abi, hector_contract_address
from web3.gas_strategies.time_based import medium_gas_price_strategy
from hector import get_config
from swap.router_addresses import spooky_router
from config import *
from addresses.ftm_addresses import token_address_dict, ftm_provider, hector_abi, comb_contract_address

if __name__ == "__main__":

    config_object:Config = get_config()

    web3 = Web3(Web3.HTTPProvider(ftm_provider))

    txManager = TransactionManager(
        key = config_object.fantom_key,
        wallet_address = config_object.wallet
    )

    swap: Swap = Swap(
        web3 = web3,
        txManager=txManager,
        wallet_address = config_object.wallet,
        router_address = spooky_router
    )

    SYMBOL = 'BEETS'

    balance = swap.get_balance(
        coin_name=SYMBOL,
        wallet_address=config_object.wallet
    )

    print(f"Recovered balance: {balance}")
    
    amount = swap.getAmountsOut(666025450995815107, token_address_dict[SYMBOL], token_address_dict["FTM"])

    print(f"getAmountsOut {amount}")

    exit(0)
    swap.swap(
        amount=0.001609807,
        input=token_address_dict['HEC'],
        output=token_address_dict['DAI']
    )
