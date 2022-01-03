from web3 import Web3
import time
from addresses.bsc_addresses import bsc_token_address_dict, bsc_provider, lp_static_busd_contract_address, lp_static_busd_abi, share_contract_address, charge_abi
from swap.swap import *
from profile_executor import *
from config import *
from swap.router_addresses import pancake_router

class ChargeDefi:
    def __init__(self, 
                        web3,
                        swap,
                        txManager,
                        profileExecutor,
                        defiStatus,
                        wallet
                        ):
        self.web3 = web3

        self.charge = web3.eth.contract(address=Web3.toChecksumAddress(lp_static_busd_contract_address), abi=lp_static_busd_abi)
        self.lp_stake = web3.eth.contract(address=Web3.toChecksumAddress(share_contract_address), abi=charge_abi)

        self.swap:Swap = swap
        self.txManager:TransactionManager = txManager
        self.profileExecutor:ProfileExecutor = profileExecutor
        self.defiStatus:DefiStatus = defiStatus
        self.wallet = wallet

    def check_stack_status(self):
        self.defiStatus.load()
        if (self.can_claim_charge() and self.can_claim_LP_stake_busd()):
            self.haverst_profit()

    def haverst_profit(self):
        self.clain_charge()
        time.sleep(5)
        self.claim_LP_stake_busd()
        time.sleep(30)
        self.profileExecutor.execute_profit(self.web3)

    def clain_charge(self):
        fnUnstake = self.charge.functions.claimReward()
        self.txManager.execute_transation(
            funTx=fnUnstake,
            web3=self.web3
        )

    def claim_LP_stake_busd(self):
        fnUnstake = self.lp_stake.functions.claimReward()
        self.txManager.execute_transation(
            funTx=fnUnstake,
            web3=self.web3
        )

    def can_claim_charge(self):
        return self.charge.functions.canClaimReward(self.wallet).call()

    def can_claim_LP_stake_busd(self):
        return self.lp_stake.functions.canClaimReward(self.wallet).call()

def get_chargeDefi():

    config_object:Config = get_config()

    web3 = Web3(Web3.HTTPProvider(bsc_provider))

    txManager = TransactionManager(
        key = config_object.fantom_key,
        wallet_address = config_object.wallet
    )

    swap: Swap = Swap(
        web3 = web3,
        txManager=txManager,
        wallet_address = config_object.wallet,
        router_address = pancake_router
    )
    
    profileExecutor = ProfileExecutor(
        txManager = txManager,
        origin_address=bsc_token_address_dict['CHARGE'],
        dest_address=bsc_token_address_dict['BUSD'],
        transaction_address=bsc_token_address_dict['BUSD'],
        swap = swap
    )
    
    return ChargeDefi(
        web3 = web3,
        swap=swap,
        txManager=txManager,
        profileExecutor = profileExecutor,
        defiStatus = DefiStatus("chargeDefi.ini"),
        wallet=config_object.wallet
    )


if __name__ == "__main__":

    chargeDefi:ChargeDefi = get_chargeDefi()

    print(chargeDefi.check_stack_status())
    
    print(chargeDefi.can_claim_charge())
    print(chargeDefi.can_claim_LP_stake_busd())

