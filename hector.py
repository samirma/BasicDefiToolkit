from web3 import Web3
import json
from configparser import ConfigParser

def get_config():
    config_object = ConfigParser()
    config_object.read("config.ini")
    return config_object

class Hector:
    def __init__(self, contract_address, wallet_address, shector_address):
        provider = "https://rpc.ftm.tools/"
        web3 = Web3(Web3.HTTPProvider(provider))
        self.web3 = web3
        self.wallet_address = wallet_address
        self.contract_address = contract_address
        self.shector_address = shector_address
        self.gas = 500080

        config_object = get_config()
        
        self.key = config_object["keys"]["hector"]

        self.shector = config_object["abis"]["shector"]
        abi_raw = config_object["abis"]["hector_staking"]

        abi = json.loads(abi_raw)
        self.contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi)


    def amount(self):
        abi = json.loads(self.shector)
        contract = self.web3.eth.contract(Web3.toChecksumAddress(self.shector_address), abi=abi)
        return contract.functions.balanceOf(self.wallet_address).call()

    def withdraw(self):

        nonce = self.web3.eth.getTransactionCount(self.wallet_address)

        web3 = self.web3

        token_tx = self.contract.functions.withdraw().buildTransaction({
                    'chainId':250, 
                    'gas': self.gas,
                    'gasPrice': web3.toWei('5','gwei'), 
                    'nonce':nonce
                })

        sign_txn = web3.eth.account.signTransaction(token_tx, private_key=self.key)
        web3.eth.sendRawTransaction(sign_txn.rawTransaction)
        print(f"Transaction has been sent to {self.main_address}")
                


def get_hector():
    config_object = get_config()
    address = config_object["address"]
    return Hector(
        contract_address=address["contract_address"],
        wallet_address=address["wallet_address"],
        shector_address=address["shector_address"]
    )


if __name__ == "__main__":

    hector = get_hector()
    print(hector.amount())

