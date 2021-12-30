from web3 import Web3
import json
from configparser import ConfigParser
import datetime
from swap.swap import *
from ftm_addresses import token_address_dict, token_abi, hector_abi, hector_contract_address
from web3.gas_strategies.time_based import medium_gas_price_strategy

def get_config():
    config_object = ConfigParser()
    config_object.read("config.ini")
    return config_object

class Hector:
    def __init__(self, 
                        key,
                        wallet_address, 
                        swap,
                        txManager
                        ):
        web3 = Web3(Web3.HTTPProvider(ftm_provider))
        self.web3 = web3
        self.wallet_address = wallet_address
        self.gas = 500080
        self.key = key
        self.contract = web3.eth.contract(address=Web3.toChecksumAddress(hector_contract_address), abi=hector_abi)
        self.hector_config_path = "hector.ini"
        
        self.section_title = "hector"
        self.last_check_module_title = "last_check"
        self.amount_title = "amount"
        self.profit_title = "profit"
        self.swap:Swap = swap
        self.txManager:TransactionManager = txManager


    def amountHec(self):
        return self.amount(token_address_dict['HEC'])

    def amountSHec(self):
        return self.amount(token_address_dict['SHEC'])

    def amount(self, address):
        contract = self.web3.eth.contract(Web3.toChecksumAddress(address), abi=token_abi)
        return contract.functions.balanceOf(self.wallet_address).call()

    def check_stack_status(self):
        #ct = datetime.datetime.now()
        #ts = ct.timestamp()
        config_object = ConfigParser()
        read_result = config_object.read(self.hector_config_path)
        
        amount = self.amountSHec()
        
        if (len(read_result) == 0):
            self.persist_update(config_object = config_object, amount = amount, profit = 0.3)
        else:
            hec_config = config_object[self.section_title]
            last_amount = float(hec_config[self.amount_title])
            profit = float(hec_config[self.profit_title])
            if (last_amount < amount):
                self.haverst_profit(last_amount, profit, amount)
                self.persist_update(config_object = config_object, amount = amount, profit = 0.3)


    def persist_update(self, config_object, amount, profit):
        print(f"new amount: {amount} profit {profit}")
        config_object[self.section_title] = {
                            self.amount_title: amount,
                            self.profit_title: profit
                        }
        with open(self.hector_config_path , 'w') as configfile:
            config_object.write(configfile)


    def haverst_profit(self, last_amount, profit, current_amount):
        if (last_amount < current_amount):
            haverst_amount = (current_amount - last_amount) * profit 
            print(f"To be havested {haverst_amount}")
            #self.unstake( haverst_amount )
            #self.swap.swap()

    def unstake(self, amount):
        fnUnstake = self.contract.functions.unstake(amount, True)
        self.txManager.execute_transation(
            funTx=fnUnstake,
            web3=self.web3,
            wallet_address=self.wallet_address,
            key=self.key
        )

def get_hector():
    config_object = get_config()
    address = config_object["address"]
    txManager=TransactionManager()
    return Hector(
        wallet_address=address["wallet_address"],
        key = config_object["keys"]["hector"],
        swap=Swap(txManager),
        txManager=txManager
    )


if __name__ == "__main__":

    hector:Hector = get_hector()
    
    print(hector.check_stack_status())

    #print(hector.unstake(156))
    #print(hector.unstake(15456900))
    print(hector.amountSHec())
    print(hector.amountHec())
    #hector.check_stack_status()
