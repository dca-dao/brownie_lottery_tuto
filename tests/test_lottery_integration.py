# Integration test are going to be on Rinkeby testnet
import time
from brownie import network, config, exceptions
from scripts.helful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    fund_with_link,
    get_contract,
)
from scripts.deploy_lottery import deploy_lottery
import pytest


def test_can_pick_winner():
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    lottery = deploy_lottery()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 1000})
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 1000})
    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()
    fund_with_link(lottery)
    # Act
    transaction = lottery.endLottery({"from": account})
    time.sleep(300)
    # Assert
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_lottery
