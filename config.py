from configparser import ConfigParser


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


