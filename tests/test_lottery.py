from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    fund_with_link,
    get_contract,
)
from brownie import Lottery, accounts, config, network, exceptions
from scripts.lottery import deploy_lottery
from web3 import Web3
import pytest
import time

def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    expected_entrance_fee = Web3.toWei(0.0125, "ether")
    entrance_fee = lottery.getLotteryPriceInWei()
    assert expected_entrance_fee == entrance_fee


def test_cant_enter_unless_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getLotteryPriceInWei()})


def test_can_start_and_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.start({"from": account})
    lottery.enter({"from": account, "value": lottery.getLotteryPriceInWei()})
    assert lottery.players(0) == account


def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.start({"from": account})
    lottery.enter({"from": account, "value": lottery.getLotteryPriceInWei()})
    fund_with_link(lottery)
    lottery.end({"from": account})
    assert lottery.status() == 2


def test_can_pick_winner_correctly():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.start({"from": account})
    lottery.enter({"from": account, "value": lottery.getLotteryPriceInWei()})
    lottery.enter({"from": get_account(index=1), "value": lottery.getLotteryPriceInWei()})
    lottery.enter({"from": get_account(index=2), "value": lottery.getLotteryPriceInWei()})
    fund_with_link(lottery)
    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()
    transaction = lottery.end({"from": account})
    request_id = transaction.events["RequestedWithId"]["requestId"]
    STATIC_RNG = 69420
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottery.address, {"from": account}
    )
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_lottery


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.start({"from": account})
    lottery.enter({"from": account, "value": lottery.getLotteryPriceInWei()})
    lottery.enter({"from": account, "value": lottery.getLotteryPriceInWei()})
    fund_with_link(lottery)
    lottery.end({"from": account})
    time.sleep(180)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0