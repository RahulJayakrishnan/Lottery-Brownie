from brownie import Lottery, accounts;
from scripts.utils import get_account;


def get_lottery_price():
    lottery = Lottery.deploy("0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419", {"from": get_account()}, publish_source=False)
    print(lottery.getLotteryPriceInWei())


def main():
    get_lottery_price()
