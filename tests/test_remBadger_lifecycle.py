import brownie
from brownie import *
from helpers.constants import MaxUint256
from helpers.SnapshotManager import SnapshotManager
from helpers.time import days

"""
  TODO: Put your tests here to prove the strat is good!
  See test_harvest_flow, for the basic tests
  See test_strategy_permissions, for tests at the permissions level
"""
def test_lifecycle_for_rem_badger(deployer, sett, strategy, controller, want, governance):
    # Setup
    startingBalance = want.balanceOf(deployer)

    depositAmount =  600_000e18 ## 600k BADGER

    restOfTokens =  600_000e18 ## 600k BADGER
    assert startingBalance >= depositAmount
    assert startingBalance >= 0
    # End Setup

    assert want.balanceOf(sett) == 0

    want.approve(sett, MaxUint256, {"from": deployer})
    ## Works
    sett.deposit(depositAmount, {"from": deployer})

    assert sett.getPricePerFullShare() == 1e18

    ## Mint200k more shares
    sett.mintExtra(2000e18, {"from": governance})

    last_ppfs = sett.getPricePerFullShare()
    assert last_ppfs < 1e18 ## We diluted

    sett.addWant(restOfTokens, {"from": deployer})

    assert sett.getPricePerFullShare() > last_ppfs