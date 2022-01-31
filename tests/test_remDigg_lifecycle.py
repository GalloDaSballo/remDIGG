import brownie
from brownie import *
from helpers.constants import MaxUint256
from helpers.SnapshotManager import SnapshotManager
from helpers.time import days

"""
  remBadger Lifecycle test
  -> Deploy
  -> Issue 52.94 shares
  -> Check ppfs
  -> Do restitution deposit
  -> Verify shares are 1to1
"""
TO_MINT = 52.94e9 ## 9 Decimals for DIGG
TO_SEED = 52.94e9 ## 9 Decimals for DIGG

def test_lifecycle_for_rem_badger(deployer, sett, strategy, controller, want, governance):
    # Setup
    startingBalance = want.balanceOf(deployer)

    depositAmount = TO_MINT
    assert startingBalance >= depositAmount
    # End Setup

    assert want.balanceOf(sett) == 0

    assert sett.getPricePerFullShare() == 1e18 ## Vault is 18 decimals
    assert sett.totalSupply() == 0

    print("Initial ppfs")
    print(1e18)

    ## Mint 2k more shares
    sett.mintExtra(TO_SEED, {"from": governance})

    assert sett.totalSupply() == TO_SEED

    last_ppfs = sett.getPricePerFullShare()
    assert last_ppfs == 0 ## Diluted with no shares

    print("Diluted PPFS")
    print(last_ppfs)

    want.transfer(sett, depositAmount, {"from": deployer})

    assert sett.getPricePerFullShare() == 1e18 ## Restitution has happened