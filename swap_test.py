from web3 import Web3
import json
from configparser import ConfigParser
import datetime
from swap.swap import *
from ftm_addresses import token_address_dict, token_abi, hector_abi, hector_contract_address
from web3.gas_strategies.time_based import medium_gas_price_strategy
from hector import get_config
from ftm_addresses import factory_addresses, router_addresses

if __name__ == "__main__":
    swap: Swap = Swap(
        txManager=TransactionManager()
    )

    config_object = get_config()
    address = config_object["address"]
    wallet_address = address["wallet_address"]
    
    key = config_object["keys"]["hector"]

    SYMBOL = 'DAI'

    balance = swap.get_balance(
        coin_name=SYMBOL,
        wallet_address=wallet_address
    )

    print(f"Recovered balance: {balance}")
    print(swap.convert_amount_to_swap(0.9999999, token_address_dict[SYMBOL]))
    
    human_balance = swap.convert_amount_to_human(balance, token_address_dict[SYMBOL])

    print(f"Human from balance {human_balance}")

    #print(swap.web3.eth.get_transaction('0xafa261a50bfed88737a4d8482ddb3c72e1eeae7b74a64921e84939ae008ac2a2'))
    buy_amount = swap.convert_amount_to_swap(0.01, token_address_dict[SYMBOL])
    print(f"###### {buy_amount}")


    #exit(0)
    swap.swap(
        wallet_address = wallet_address,
        amount=0.1,
        input='DAI',
        output='HEC',
        key = key
    )
