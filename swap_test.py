from web3 import Web3
import json
from configparser import ConfigParser
import datetime
from swap.swap import *
from ftm_addresses import token_address_dict, token_abi, hector_abi, hector_contract_address
from web3.gas_strategies.time_based import medium_gas_price_strategy
from hector import get_config


if __name__ == "__main__":
    swap: Swap = Swap()

    config_object = get_config()
    address = config_object["address"]
    wallet_address = address["wallet_address"]
    
    key = config_object["keys"]["hector"]

    SYMBOL = 'DAI'

    balance = swap.get_balance(
        coin_name=SYMBOL,
        wallet_address=wallet_address
    )

    print(swap.convert_amount_to_swap(balance, token_address_dict[SYMBOL]))
    print(swap.convert_amount_to_human(balance, token_address_dict[SYMBOL]))

    print(swap.web3.eth.gasPrice)

    #exit(0)
    swap.swap(
        wallet_address = wallet_address,
        amount=5997853254560781000000000000000000,
        input='DAI',
        output='HEC',
        key = key
    )
