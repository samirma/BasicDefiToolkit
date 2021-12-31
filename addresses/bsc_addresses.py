import json
import os

def load_abi(abi_filename):
    #with open(os.path.join(os.path.dirname(working_path), 'abi', abi_filename)) as f:
    with open(os.path.join('./abi', abi_filename)) as f:
        return json.load(f)

token_abi = load_abi("token.abi")
pairs_abi = load_abi("pairs.abi")
router_abi = load_abi("router.abi")
factory_abi = load_abi("factory.abi")

lp_static_busd_abi = load_abi("lp_static_busd.abi")
charge_abi = load_abi("charge.abi")

lp_static_busd_contract_address = "0x7692bCB5F646abcdFA436658dC02d075856ac33C"
share_contract_address = "0x53D55291c12EF31b3f986102933177815DB72b3A"

bsc_provider =  "https://bsc-dataseed.binance.org/"

bsc_token_address_dict = {
    'CHARGE': "0x1C6bc8e962427dEb4106aE06A7fA2d715687395c",
    'STATIC': "0x7dEb9906BD1d77B410a56E5C23c36340Bd60C983",
    'PULSE': "0xbceBAeAF1160Edc84D81A8f2D075858eE3960e9E",
    'BUSD': "0xe9e7cea3dedca5984780bafc599bd69add087d56",
    'TITANO': "0xBA96731324dE188ebC1eD87ca74544dDEbC07D7f"
}

