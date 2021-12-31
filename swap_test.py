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

    config_object = get_config()
    address = config_object["address"]
    wallet_address = address["wallet_address"]
    
    key = config_object["keys"]["hector"]

    swap: Swap = Swap(
        txManager=TransactionManager(),
        key = key,
        wallet_address = wallet_address
    )

    SYMBOL = 'HEC'

    balance = swap.get_balance(
        coin_name=SYMBOL,
        wallet_address=wallet_address
    )

    print(f"Recovered balance: {balance}")
    
    human_balance = swap.convert_amount_to_human(115892, token_address_dict['FTM'])

    print(f"Human from balance {human_balance}")

    transaction_hash = '0x543a6f77957c174390a39132b4b8d1c7bf5c4ea58a165c02ef624855aeb70d70'

    gas_price = swap.web3.eth.getTransaction(transaction_hash).gasPrice
    gas_used = swap.web3.eth.getTransactionReceipt(transaction_hash).gasUsed

    transaction_cost = gas_price * gas_used

    #print(swap.web3.eth.get_transaction('0x543a6f77957c174390a39132b4b8d1c7bf5c4ea58a165c02ef624855aeb70d70'))

    print(f"###### {transaction_cost} -> {swap.convert_amount_to_human(transaction_cost, token_address_dict['FTM'])}")

    exit(0)
    swap.swap(
        amount=0.001609807,
        input=token_address_dict['HEC'],
        output=token_address_dict['DAI']
    )
