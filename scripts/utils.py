from brownie import config, accounts, network, MockV3Aggregator

DECIMALS = 8
PRICE = 4000 * 10 ** DECIMALS


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    if len(MockV3Aggregator) > 0:
        return
    print("deploying Mocks...")
    MockV3Aggregator.deploy(DECIMALS, PRICE, {"from": get_account()})
