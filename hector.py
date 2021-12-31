from web3 import Web3
import time
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
        self.defiStatus.load()
        
        amount = self.amountSHec()
        
        if (self.defiStatus.is_first()):
            print("First read")
            self.defiStatus.save(amount = amount, profit = 0.3)
        else:
            last_amount = self.defiStatus.amount
            profit = self.defiStatus.profit
            print(f"{last_amount} < {amount}")
            if (last_amount < amount):
                self.haverst_profit(last_amount, profit, amount)
                self.defiStatus.save(amount = amount, profit = 0.3)

    def haverst_profit(self, last_amount, profit, current_amount):
        haverst_amount = int((current_amount - last_amount) * profit)
        print(f"To be havested {haverst_amount}")
        if (last_amount < current_amount):
            self.unstake( haverst_amount )
            time.sleep(30)
            self.profileExecutor.execute_profit(self.web3)

    def unstake(self, amount):
        fnUnstake = self.contract.functions.unstake(amount, True)
        self.txManager.execute_transation(
            funTx=fnUnstake,
            web3=self.web3
        )

def get_hector():

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
