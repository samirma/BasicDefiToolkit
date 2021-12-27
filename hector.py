from web3 import Web3
import json
from configparser import ConfigParser
import datetime
from swap.swap import *
from ftm_addresses import token_address_dict, token_abi, hector_abi
from web3.gas_strategies.time_based import medium_gas_price_strategy

def get_config():
    config_object = ConfigParser()
    config_object.read("config.ini")
    return config_object

def string_to_bytes32(data):
    if len(data) > 32:
        myBytes32 = data[:32]
    else:
        myBytes32 = data.ljust(32, '0')
    return bytes(myBytes32, 'utf-8')


class Hector:
    def __init__(self, 
                        key,
                        contract_address, 
                        wallet_address, 
                        swap,
                        ):
        provider = "https://rpc.ftm.tools/"
        web3 = Web3(Web3.HTTPProvider(provider))
        self.web3 = web3
        self.wallet_address = wallet_address
        self.contract_address = contract_address
        self.gas = 500080
        self.key = key
        self.contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=hector_abi)
        self.hector_config_path = "hector.ini"
        
        self.section_title = "hector"
        self.last_check_module_title = "last_check"
        self.amount_title = "amount"
        self.profit_title = "profit"

        self.swap :Swap = swap


    def amountHec(self):
        return self.amount(token_address_dict['HEC'])

    def amountSHec(self):
        return self.amount(token_address_dict['SHEC'])

    def amount(self, address):
        contract = self.web3.eth.contract(Web3.toChecksumAddress(address), abi=token_abi)
        return contract.functions.balanceOf(self.wallet_address).call()

    def check_stack_status(self):
        ct = datetime.datetime.now()
        ts = ct.timestamp()
        config_object = ConfigParser()
        read_result = config_object.read(self.hector_config_path)
        if (len(read_result) == 0):
            amount = self.amount()
            config_object[self.section_title] = {self.last_check_module_title: ts,
                                self.amount_title: amount,
                                self.profit_title: 0.3}
            with open(self.hector_config_path , 'w') as configfile:
                config_object.write(configfile)
        else:
            last_check = config_object[self.last_check_module_title]
            last_amount = config_object[self.amount_title]
            profit = config_object[self.profit_title]
            self.haverst_profit(last_check, last_amount, profit)

    def unstake(self, amount):
        self.web3.eth.setGasPriceStrategy(medium_gas_price_strategy)

        nonce = self.web3.eth.getTransactionCount(self.wallet_address)
        web3 = self.web3
        token_tx = self.contract.functions.unstake(12345, True).buildTransaction(
                {
                #    'chainId':250, 
                    'gas':2000000,
                    'nonce':nonce
                }
            )

        sign_txn = web3.eth.account.signTransaction(token_tx, self.key)
        tx_hash = web3.eth.sendRawTransaction(sign_txn.rawTransaction)
        return tx_hash


    def haverst_profit(self, last_check, last_amount, profit):
        current_amount = self.amount()
        if (last_amount < current_amount):
            self.unstake( (current_amount - last_amount) * profit )
            self.swap.swap()



def get_hector():
    config_object = get_config()
    address = config_object["address"]
    return Hector(
        contract_address=address["contract_address"],
        wallet_address=address["wallet_address"],
        key = config_object["keys"]["hector"],
        swap=Swap(),
    )


if __name__ == "__main__":

    hector:Hector = get_hector()
    print(hector.unstake(154569))
    print(hector.amountSHec())
    #print(hector.amountHec())
    #hector.check_stack_status()
