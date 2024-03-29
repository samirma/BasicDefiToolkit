from web3 import Web3
from swap.swap import *
from addresses.ftm_addresses import token_address_dict, ftm_provider, hector_abi, comb_contract_address
from profile_executor import *
from config import *
from swap.router_addresses import spooky_router
import time

class Comb:
    def __init__(self, 
                        web3,
                        swap,
                        txManager,
                        defiStatus
                        ):
        self.web3 = web3
        self.contract = web3.eth.contract(address=Web3.to_checksum_address(comb_contract_address), abi=hector_abi)

        self.swap:Swap = swap
        self.txManager:TransactionManager = txManager
        self.defiStatus:DefiStatus = defiStatus


    def amount(self, token_address):
        return self.swap.get_balance_by_address(token_address, wallet_address=self.swap.wallet_address)

    def sell(self, origin, dest):
        origin_address = token_address_dict[origin]
        dest_address = token_address_dict[dest]
        
        balance = self.amount(origin_address)

        if (balance == 0):
            print(f"No balance {balance}")
            return
        
        print(f"Swap {balance} from {origin} to {dest}")

        r = self.swap.select_contract(1, origin_address, dest_address)

        print(r)
 
        self.swap.swap(
            amount=balance,
            input=origin_address,
            output=dest_address
        )

    def sell_all(self):
        dest_address = 'USDC'
        self.sell('SPIRIT', dest_address)
        #self.sell('SCREAM', dest_address)
        self.sell('COMB', dest_address)
        self.sell('BEETS', dest_address)
        self.sell('BOO', dest_address)


    def claim(self):
        fnUnstake = self.contract.functions.claim()
        self.txManager.execute_transation(
            funTx=fnUnstake,
            web3=self.web3
        )
        time.sleep(10)

def get_comb():

    config_object:Config = get_config()

    web3 = Web3(Web3.HTTPProvider(ftm_provider))

    txManager = TransactionManager(
        key = config_object.fantom_key,
        wallet_address = config_object.wallet
    )

    swap: Swap = Swap(
        web3 = web3,
        txManager=txManager,
        wallet_address = config_object.wallet
    )
    
    return Comb(
        web3 = web3,
        swap=swap,
        txManager=txManager,
        defiStatus = DefiStatus("comb.ini")
    )


if __name__ == "__main__":

    comb:Comb = get_comb()
    
    #comb.claim()
    
    #time.sleep(3)
    
    comb:Comb = get_comb()

    comb.sell_all()


