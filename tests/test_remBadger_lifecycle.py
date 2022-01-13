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
    assert sett.getPricePerFullShare() == 1e18
    assert sett.totalSupply() == 0

    print("Initial ppfs")
    print(1e18)

    ## Mint 2k more shares
    sett.mintExtra(2000e18, {"from": governance})

    assert sett.totalSupply() == 2000e18

    last_ppfs = sett.getPricePerFullShare()
    assert last_ppfs < 1e18 ## We diluted

    print("Diluted PPFS")
    print(1e18)

    sett.addWant(depositAmount, {"from": deployer})

    assert sett.getPricePerFullShare() > last_ppfs
    last_ppfs = sett.getPricePerFullShare()

    print("New ppfs 1")
    print(sett.getPricePerFullShare())

    sett.addWant(restOfTokens, {"from": deployer})

    assert sett.getPricePerFullShare() > last_ppfs

    print("New ppfs 2")
    print(sett.getPricePerFullShare())