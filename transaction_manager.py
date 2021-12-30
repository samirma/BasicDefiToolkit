from web3 import Web3


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
    
    def execute_transation(self, funTx, web3: Web3, wallet_address, key):
        nonce = web3.eth.getTransactionCount(wallet_address)
        tx = funTx.buildTransaction({
            'from': wallet_address,
            'gas': funTx.estimateGas(),
            'nonce': nonce,
            "gasPrice": web3.eth.gas_price
        })
        signed_tx = web3.eth.account.signTransaction(tx, key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        hashes = Web3.toHex(tx_hash)
        web3.eth.waitForTransactionReceipt(tx_hash)
        status = web3.eth.get_transaction_receipt(hashes)
        txStatus = status.status
        success = int(txStatus) == 1
        if success:
            print(style.YELLOW+"SuccessFully {}".format(hashes)+style.RESET)
        else:
            print(style.MAGENTA+"TRANSACTION FAILED !!"+style.RESET)
        
        return success
