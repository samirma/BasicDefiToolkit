from web3 import Web3
from web3.contract import ContractFunction

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

class TransactionManager:

    def __init__(self, wallet_address, key):
        self.transactions = []
        self.wallet_address = wallet_address
        self.key = key
    
    def execute_transation(self, funTx: ContractFunction, web3: Web3):

        print(f"Key {self.key} Wallet {self.wallet_address}")

        nonce = web3.eth.getTransactionCount(self.wallet_address)
        tx = funTx.buildTransaction({
            'from': self.wallet_address,
            'gas': web3.eth.estimateGas(funTx),
            'gasPrice': web3.eth.generateGasPrice(funTx),
            #'gas': funTx.estimateGas({"from": self.wallet_address, "gasPrice": web3.eth.gas_price}),
            #"gasPrice": web3.eth.gas_price,
            'nonce': nonce
        })
        signed_tx = web3.eth.account.signTransaction(tx, self.key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        hashes = Web3.toHex(tx_hash)
        web3.eth.waitForTransactionReceipt(tx_hash)
        status = web3.eth.get_transaction_receipt(hashes)
        txStatus = status.status
        success = int(txStatus) == 1
        if success:
            print(style.GREEN+"TRANSACTION Successed {}".format(hashes)+style.RESET)
        else:
            print(style.MAGENTA+"TRANSACTION FAILED !!"+style.RESET)


        self.save_transaction_fee(hashes)
        
        return success

    def save_transaction_fee(self, transaction_hash):
        self.transactions.append(transaction_hash)

    def get_transaction_fee(self, web3: Web3, transaction_hash):
        gas_price = web3.eth.getTransaction(transaction_hash).gasPrice
        gas_used = web3.eth.getTransactionReceipt(transaction_hash).gasUsed
        transaction_cost = gas_price * gas_used
        return transaction_cost

    def get_total_fees(self, web3: Web3):
        fees = 0
        for x in self.transactions:
            fees += self.get_transaction_fee(web3, x)
        return fees
