from configparser import ConfigParser

from web3._utils.rpc_abi import TRANSACTION_PARAMS_ABIS

PROFIT = 0.3
AMOUNT = -1
TRANSACTION_SPENT = 0

class DefiStatus:
    def __init__(self, 
                file_path,
                ):
        self.profit = PROFIT
        self.amount = AMOUNT
        self.transactions_spent = TRANSACTION_SPENT
        self.file_path = file_path
        self.config_object :ConfigParser = ConfigParser()

        self.section_title = "status"
        self.last_check_module_title = "last_check"
        self.amount_title = "amount"
        self.profit_title = "profit"
        self.transactions_spent_title = "transaction_spent"


    def is_first(self):
        return self.amount == AMOUNT

    def load(self):
        self.config_object.read(self.file_path)
        print(f"Status loaded from {self.file_path}")
        self.amount = self.config_object.getfloat(self.section_title, self.amount_title, fallback=AMOUNT)
        self.profit = self.config_object.getfloat(self.section_title, self.profit_title, fallback=PROFIT)
        self.transactions_spent = self.config_object.getfloat(self.section_title, self.profit_title, fallback=TRANSACTION_SPENT)

    def save(self, profit, amount, transactions_spent):
        self.profit = profit
        self.amount = amount
        self.transactions_spent = transactions_spent
        print(f"new amount: {amount} profit {profit}")
        self.config_object[self.section_title] = {
                            self.amount_title: amount,
                            self.profit_title: profit,
                            self.transactions_spent_title: transactions_spent
                        }
        with open(self.file_path , 'w') as configfile:
            self.config_object.write(configfile)


class Config:
    def __init__(self, 
                        fantom_key,
                        wallet
                        ):
        self.wallet = wallet
        self.fantom_key = fantom_key

def get_config():
    config_object = ConfigParser()
    config_object.read("config.ini")

    wallet_address = config_object["address"]["wallet_address"]
    key = config_object["keys"]["fantom"]

    return Config(fantom_key=key, wallet=wallet_address)


if __name__ == "__main__":

    exit(0)
    print(get_config().fantom_key)
    print(get_config().wallet)

    status = DefiStatus("hector.ini")
    assert(status.is_first())

    status.load()
    assert(status.is_first())

    print(status.last_amount)
    print(status.profit)

    status.save(profit=0.5, amount=0.555)

    print(status.last_amount)
    print(status.profit)

    assert(not status.is_first())

