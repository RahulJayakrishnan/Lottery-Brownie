from brownie import Lottery, config, network;
from scripts.helpful_scripts import get_account, get_contract, fund_with_link


def deploy_lottery():
    lottery = Lottery.deploy(get_contract("eth_usd_price_feed").address,
                             config["networks"][network.show_active()]["keyhash"],
                             get_contract("vrf_coordinator").address,
                             get_contract("link_token").address,
                             config["networks"][network.show_active()]["fee"],
                             {"from": get_account()},
                             publish_source=config["networks"][network.show_active()].get("verify", False))
    print("deployed lottery....")

    return lottery


def start_lottery():
    lottery = Lottery[-1]
    print("starting lottery....")
    tx = lottery.start({"from": get_account()})
    tx.wait(1)


def enter_lottery():
    lottery = Lottery[-1]
    min_value = lottery.getLotteryPriceInWei()
    tx = lottery.enter({"from": get_account(),
                        "value": min_value})
    tx.wait(1)
    print("lottery entered....")


def end_lottery():
    lottery = Lottery[-1]
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    tx = lottery.end({"from": get_account()})
    tx.wait(1)


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
