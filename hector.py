from web3 import Web3
import json
import datetime
from swap.swap import *
from ftm_addresses import token_address_dict, token_abi, hector_abi, hector_contract_address
from profile_executor import *
from config import *

class Hector:
    def __init__(self, 
                        swap,
                        txManager,
                        profileExecutor,
                        defiStatus
                        ):
        web3 = Web3(Web3.HTTPProvider(ftm_provider))
        self.web3 = web3
        self.gas = 500080
        self.contract = web3.eth.contract(address=Web3.toChecksumAddress(hector_contract_address), abi=hector_abi)

        self.swap:Swap = swap
        self.txManager:TransactionManager = txManager
        self.profileExecutor:ProfileExecutor = profileExecutor
        self.defiStatus:DefiStatus = defiStatus


    def amountSHec(self):
        return self.swap.get_balance_by_address(token_address_dict['SHEC'], wallet_address=self.swap.wallet_address)

    def check_stack_status(self):
        #ct = datetime.datetime.now()
        #ts = ct.timestamp()
        self.defiStatus.load()
        
        amount = self.amountSHec()
        
        if (self.defiStatus.is_first()):
            self.defiStatus.save(amount = amount, profit = 0.3)
        else:
            last_amount = self.defiStatus.last_amount
            profit = self.defiStatus.profit
            if (last_amount < amount):
                self.haverst_profit(last_amount, profit, amount)
                self.defiStatus.save(amount = amount, profit = 0.3)

    def haverst_profit(self, last_amount, profit, current_amount):
        haverst_amount = (current_amount - last_amount) * profit 
        print(f"To be havested {haverst_amount}")
        if (last_amount < current_amount and False):
            self.unstake( haverst_amount )
            self.profileExecutor.execute_profit(self.web3)

    def unstake(self, amount):
        fnUnstake = self.contract.functions.unstake(amount, True)
        self.txManager.execute_transation(
            funTx=fnUnstake,
            web3=self.web3,
            wallet_address=self.wallet_address,
            key=self.key
        )

def get_hector():
    config_object:Config = get_config()
    txManager = TransactionManager()

    swap: Swap = Swap(
        txManager=txManager,
        key = config_object.fantom_key,
        wallet_address = config_object.wallet
    )

    
    profileExecutor = ProfileExecutor(
        txManager = txManager,
        origin_address=token_address_dict['HEC'],
        dest_address=token_address_dict['DAI'],
        transaction_address=token_address_dict['FTM'],
        swap = swap
    )
    
    return Hector(
        swap=swap,
        txManager=txManager,
        profileExecutor = profileExecutor,
        defiStatus = DefiStatus("hector.ini")
    )


if __name__ == "__main__":

    hector:Hector = get_hector()
    
    print(hector.check_stack_status())

    #print(hector.unstake(156))
    #print(hector.unstake(15456900))
    #print(hector.amountSHec())
    #hector.check_stack_status()
