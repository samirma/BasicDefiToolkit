""" Get the price of a token on a dex.
"""
from web3 import Web3
import sys
import os
import pathlib
from addresses.ftm_addresses import token_address_dict, ftm_provider, factory_abi, pairs_abi
from profile_executor import *
from config import *
from swap.router_addresses import spooky_router, spooky_factory, spirit_factory, spirit_router
import math
weth_decimal = 18

def getprice(web3, 
            router_address,
            token_address, 
            factory_address, 
            weth_address, 
            eth_in=1, 
            weth_decimal=18,
            verbose=True):
    """ Returns bid price, ask price.
        Bid price is how much they will give you in fantom for the token.
        Ask price is how much fantom you need to give for the token.
    """
    try:
        token_contract = web3.eth.contract(address=token_address, abi=token_abi)
        weth_contract = web3.eth.contract(address=weth_address, abi=token_abi)
        decimal = token_contract.functions.decimals().call()
        factory_contract = web3.eth.contract(address=web3.toChecksumAddress(factory_address), abi=factory_abi)
        pair_address = factory_contract.functions.getPair(token_address, weth_address).call()
        pair_contract = web3.eth.contract(address=web3.toChecksumAddress(pair_address), abi=pairs_abi)
        # Check is this pair on this dex
        # web3.eth.getCode
        token0_address = pair_contract.functions.token0().call()
        token1_address = pair_contract.functions.token1().call()
        reserves = pair_contract.functions.getReserves().call()
        if token0_address == weth_address:
            reserves_price = reserves[0]/reserves[1]
        elif token1_address == weth_address:
            reserves_price = reserves[1]/reserves[0]
        else:
            return("Error matching weth equivalent")
        adjusted_reserves_price = (reserves_price)  * (math.pow(10, weth_decimal)) / (reserves[1] / math.pow(10, decimal))
        eth_in_wei = web3.toWei(eth_in, 'Ether')
        router_contract = web3.eth.contract(address=web3.toChecksumAddress(router_address), abi=router_abi)
        # First call: for a given FTM input, find how much token we get out
        amount_out_token = router_contract.functions.getAmountsOut(eth_in_wei, [weth_address, token_address]).call()
        ask_price_wei = eth_in_wei / amount_out_token[1]
        ask_price_ftm = ask_price_wei * ( math.pow(10, decimal) / math.pow(10, weth_decimal))
        adjusted_token_out = amount_out_token[1] * math.pow(10, -decimal)
        # Second call: selling this amount of eth back, how much token do we get?
        tokens_in = amount_out_token[1]
        amount_out_ftm = router_contract.functions.getAmountsOut(tokens_in, [token_address, weth_address]).call()
        bid_price_wei =  amount_out_ftm[1] /tokens_in   # price is in the input units
        bid_price_ftm = bid_price_wei * (math.pow(10, decimal) / math.pow(10, weth_decimal))
        if verbose:
            token_symbol = token_contract.functions.symbol().call()
            weth_contract = weth_contract.functions.symbol().call()
            print("getprice: {} {} gets you {} {}".format(eth_in, weth_contract, adjusted_token_out, token_symbol))
            print("getprice: {} {} gets you {} {}".format(adjusted_token_out, token_symbol, amount_out_ftm[1]/math.pow(10, weth_decimal), weth_contract))
            print("Price  Reserves: {} , Bid: {} Ask: {}".format(adjusted_reserves_price, bid_price_ftm, ask_price_ftm))
        return(bid_price_wei, ask_price_wei, ask_price_ftm, bid_price_ftm)
    except Exception as e:
        print("Contract error " + str(e))

if __name__ == '__main__':
    web3 = Web3(Web3.HTTPProvider(ftm_provider))
    token_symbol = 'HEC'

    origin_address=token_address_dict[token_symbol]

    weth_address=token_address_dict['DAI']

    margin = 0.01

    try:
        print("###### spooky ###### ")
        bid_price1, ask_price1, bid_price1_ftm, ask_price1_ftm = getprice(web3, 
                                                                            token_address=origin_address, 
                                                                            factory_address=spooky_factory, 
                                                                            router_address=spooky_router,
                                                                            weth_address=weth_address
                                                                            )
    except:
        print("Failed to get price for {} from {}".format(token_symbol, "spooky"))
    try:
        print("###### spirit ###### ")
        bid_price2, ask_price2, bid_price2_ftm, ask_price2_ftm = getprice(web3, 
                                                                            token_address=origin_address, 
                                                                            factory_address=spirit_factory, 
                                                                            router_address=spirit_router,
                                                                            weth_address=weth_address
                                                                            )
    except:
        print("Failed to get price for {} from {}".format(token_symbol, "spirit"))
    # If we got here then we have two prices.
    # We want an ask less than a bid, which is to say we want to pay
    # a smaller amount, and receive a larger amount
    print("ask 1: {:6f} bid 2: {:6f}, {:2.2f}% difference".format(
            ask_price1, bid_price2, 100*(ask_price1 - bid_price2)/ask_price1))
    print("ask 2: {} bid 1: {}, {}% difference".format(
            ask_price2, bid_price1, 100*(ask_price2 - bid_price1)/ask_price2))

    scale = 1.0 - margin
    potential_trade = False

    if (ask_price1_ftm < (bid_price2_ftm * scale)):
        print("Potential trade found")
        # we can buy on dex1 for less than dex2 will sell to us
        #dexlo, dexhi = dex1, dex2
        ask_price, bid_price = ask_price1, bid_price2
        potential_trade = True

    elif (ask_price2_ftm < (bid_price1_ftm * scale)):
        print("Potential trade found")
        # we can buy on dex2 for less than dex1 will sell to us
        #dexlo, dexhi = dex2, dex1
        ask_price, bid_price = ask_price2, bid_price1
        potential_trade = True 
    else:
        print("ask {} bidscale {}".format(ask_price2_ftm, bid_price1_ftm * scale))
        #dexlo, dexhi = dex2, dex1
        ask_price, bid_price = ask_price2, bid_price1
        potential_trade = False
 