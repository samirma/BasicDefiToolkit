from web3 import Web3
from transaction_manager import * 
from addresses.ftm_addresses import token_abi, router_abi
from addresses.ftm_addresses import token_address_dict
from time import sleep, time
from swap.router_addresses import spooky_router, spirit_router

class Swap:

    def __init__(self,
                web3,
                txManager,
                wallet_address
            ):
        self.web3 = web3
        self.txManager:TransactionManager = txManager
        self.wallet_address = wallet_address

    def swap(self,
            amount, 
            input, 
            output 
        ):
        web3 = self.web3
        
        self.buy(web3, 
                token_address_in = input, 
                token_address_out = output, 
                amount=amount
                )

    def get_path(self, token_address_in, token_address_out):
        path = [Web3.toChecksumAddress(token_address_in), Web3.toChecksumAddress(token_address_dict["FTM"])]

        if (token_address_dict["FTM"] != token_address_out):
            path.append(Web3.toChecksumAddress(token_address_out))
        return path

    def getAmountsOut(self, amount, token_address_in, token_address_out, router):
        amount_out = 0
        try:
            result = router.functions.getAmountsOut(amount, 
                            self.get_path(token_address_in, token_address_out)
                            ).call()
            amount_out = result[-1]
        except:
            print("An exception occurred")        

        return amount_out

    def select_contract(self, amount, token_address_in, token_address_out):
        print(f"Select {amount}")
        c1 = self.web3.eth.contract(address=self.web3.toChecksumAddress(spooky_router), abi=router_abi)
        c2 = self.web3.eth.contract(address=self.web3.toChecksumAddress(spirit_router), abi=router_abi)

        m1 = self.getAmountsOut(amount, token_address_in, token_address_out, c1)
        m2 = self.getAmountsOut(amount, token_address_in, token_address_out, c2)
        
        if (m1 > m2):
            print(f"Selected {m1}  > {m2}")
            return c1
        else:
            print(f"Selected {m2}  > {m1}")
            return c2


    def buy(self, 
                web3, 
                token_address_in, 
                token_address_out,
                amount
                ):

        router = self.select_contract(amount, token_address_in, token_address_out)
        amount_out = self.getAmountsOut(amount, token_address_in, token_address_out, router)

        min_tokens = int(amount_out * (1 - (50 / 100)))
        
        print(amount_out)

        funSwap = router.functions.swapExactTokensForTokens(
            amount,
            min_tokens,
            self.get_path(token_address_in, token_address_out),
            Web3.toChecksumAddress(self.wallet_address),
            deadline = int(time() + + 240)
        )

        self.txManager.execute_transation(
            funTx=funSwap,
            web3 = web3
        )

    def get_balance(self, coin_name, wallet_address):
        token_address_in = token_address_dict[coin_name]
        return self.get_balance_by_address(token_address_in = token_address_in, wallet_address = wallet_address) 
        
    def get_balance_by_address(self, token_address_in, wallet_address):
        web3 = self.web3
        token_contract_checked = web3.toChecksumAddress(token_address_in)
        wallet_address_checked = web3.toChecksumAddress(wallet_address)
        return self.get_balance_by_checked_address(token_address = token_contract_checked, wallet_address = wallet_address_checked) 
        
    def get_balance_by_checked_address(self, token_address, wallet_address):
        web3 = self.web3
        token_contract_in = web3.eth.contract(address=token_address, abi=token_abi)
        return token_contract_in.functions.balanceOf(wallet_address).call()

    def convertToSwap(self, spend_amount):
        return self.web3.toWei(str(spend_amount), 'Ether')

    def decimal_value(self, token_address):
        return self.decimal_value_by_checked_address(self.web3.toChecksumAddress(token_address))

    def decimal_value_by_checked_address(self, token_address):
        token_contract = self.web3.eth.contract(address=token_address, abi=token_abi)
        return token_contract.functions.decimals().call()

    def convert_amount_to_swap(self, amount, token_address):
        DECIMALS = self.decimals(token_address)
        amount = amount * DECIMALS
        return amount

    def convert_amount_to_human(self, amount, token_address):
        symbolDecimals = self.decimal_value(token_address)
        return amount / 10 ** symbolDecimals

    def approve_spend(self, token_address_in, router_address, wallet_address, total_max_spend=1.0):
        web3 = self.web3
        cs_router_address = web3.toChecksumAddress(router_address)
        cs_wallet_address = web3.toChecksumAddress(wallet_address)
        token_contract_in = web3.eth.contract(address=web3.toChecksumAddress(token_address_in), abi=token_abi)
        allowed = int(token_contract_in.functions.allowance(cs_wallet_address, cs_router_address).call())
        print("Approved up to {}".format(allowed))
        max_amount = int(web3.toWei(total_max_spend, 'ether'))
        if allowed < max_amount:
            self.txManager.execute_transation
        else:
            tx = 'approval exists'
        allowed = token_contract_in.functions.allowance(cs_wallet_address, cs_router_address).call()
        return(allowed, tx)

    def decimals(self, address):
        decimals = self.decimal_value(address)
        DECIMALS = 10 ** decimals
        return DECIMALS

        
