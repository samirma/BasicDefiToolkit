from configparser import ConfigParser

PROFIT = 0.3
AMOUNT = -1

class DefiStatus:
    def __init__(self, 
                file_path,
                ):
        self.profit = PROFIT
        self.amount = AMOUNT
        self.file_path = file_path
        self.config_object :ConfigParser = ConfigParser()

        self.section_title = "status"
        self.last_check_module_title = "last_check"
        self.amount_title = "amount"
        self.profit_title = "profit"


    def is_first(self):
        return self.amount == AMOUNT

    def load(self):
        self.config_object.read(self.file_path)
        self.amount = self.config_object.getfloat(self.section_title, self.amount_title, fallback=AMOUNT)
        self.profit = self.config_object.getfloat(self.section_title, self.profit_title, fallback=PROFIT)

    def save(self, profit, amount):
        self.profit = profit
        self.amount = amount
        print(f"new amount: {amount} profit {profit}")
        self.config_object[self.section_title] = {
                            self.amount_title: amount,
                            self.profit_title: profit
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

