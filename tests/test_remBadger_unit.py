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
def test_brick_permissions(deployer, sett, rando, strategist, governance):
  with brownie.reverts("onlyGovernance"):
    sett.brickDeposits({"from": strategist})

  with brownie.reverts("onlyGovernance"):
    sett.brickDeposits({"from": rando})

  sett.brickDeposits({"from": governance})

def test_mint_permissions(deployer, sett, rando, strategist, governance):
    with brownie.reverts("onlyGovernance"):
      sett.mintExtra(123, {"from": strategist})

    with brownie.reverts("onlyGovernance"):
      sett.mintExtra(123, {"from": rando})

    sett.mintExtra(123, {"from": governance})

def test_brick_blocks_mint_permissions(deployer, sett, rando, strategist, governance):
    sett.brickDeposits({"from": governance})
    
    with brownie.reverts("You can mint extra only until you brick deposits"):
      sett.mintExtra(123, {"from": governance})

def test_mint_blocks_deposits_permissions(deployer, sett, rando, strategist, governance):
    """
      Equivalent to saying you can only mint once
    """
    sett.mintExtra(123, {"from": governance})

    with brownie.reverts("You can mint extra only until you brick deposits"):
      sett.mintExtra(123, {"from": governance})

def test_brick_blocks_deposits_not_withdraw(deployer, sett, strategy, controller, want, governance):
    # Setup
    startingBalance = want.balanceOf(deployer)

    depositAmount = startingBalance // 6
    assert startingBalance >= depositAmount
    assert startingBalance >= 0
    # End Setup

    assert want.balanceOf(sett) == 0

    want.approve(sett, MaxUint256, {"from": deployer})
    ## Works
    sett.deposit(depositAmount, {"from": deployer})
    sett.withdraw(depositAmount / 10, {"from": deployer})

    sett.brickDeposits({"from": governance})

    ## Deposits are bricked, can't deposit anymore
    with brownie.reverts():
      sett.deposit(depositAmount, {"from": deployer})

    ## Can still withdraw
    sett.withdraw(depositAmount / 10, {"from": deployer})
    sett.withdrawAll({"from": deployer})

def test_mint_mints_exact(deployer, sett, strategy, controller, want, governance):
  assert sett.totalSupply() == 0

  sett.mintExtra(123, {"from": governance})

  assert sett.totalSupply() == 123


def test_mint_mints_exact_after_seeded(deployer, sett, strategy, controller, want, governance):
    # Setup
    startingBalance = want.balanceOf(deployer)

    depositAmount = startingBalance // 6
    assert startingBalance >= depositAmount
    assert startingBalance >= 0
    # End Setup

    assert want.balanceOf(sett) == 0

    want.approve(sett, MaxUint256, {"from": deployer})
    ## Works
    sett.deposit(depositAmount, {"from": deployer})

    assert sett.totalSupply() == depositAmount

    sett.mintExtra(123, {"from": governance})

    assert sett.totalSupply() == depositAmount + 123

  
def test_mint_mints_exact_after_seeded(deployer, sett, strategy, controller, want, governance):
    # Setup
    startingBalance = want.balanceOf(deployer)

    depositAmount = startingBalance // 6
    assert startingBalance >= depositAmount
    assert startingBalance >= 0
    # End Setup

    assert want.balanceOf(sett) == 0

    want.approve(sett, MaxUint256, {"from": deployer})
    ## Works
    sett.deposit(depositAmount, {"from": deployer})

    assert sett.totalSupply() == depositAmount

    sett.mintExtra(123, {"from": governance})

    assert sett.totalSupply() == depositAmount + 123