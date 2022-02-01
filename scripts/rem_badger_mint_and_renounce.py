from brownie import (
    accounts,
    network,
    BrikedStrategy,
    RemDIGG,
    AdminUpgradeabilityProxy,
    Controller,
    BadgerRegistry,
)

from config import WANT, PROTECTED_TOKENS, FEES, REGISTRY

from helpers.constants import AddressZero

import click
from rich.console import Console

console = Console()

VAULT = "0x8B2a18b6400338272FDD1B991F5163E21723AF60"
STRATEGY = "0x4055D395361E73530D43c9D4F18b0668fe4B5b91"

TO_MINT = 52.94e9 ##

RECIPIENT = "0xB65cef03b9B89f99517643226d76e286ee999e77" ## Dev Multi

def main():
    """ 
    Mint 2k shares
    Send them to Multi
    Renounce ownership of Vault and Strategy
    """

    dev = connect_account()

    v = RemDIGG.at(VAULT)
    s = BrikedStrategy.at(STRATEGY)

    v.mintExtra(TO_MINT, {"from": dev})
    v.transfer(RECIPIENT, TO_MINT, {"from": dev})

    if s.performanceFeeGovernance() != 0:
        s.setPerformanceFeeGovernance(0, {"from": dev})
    if s.performanceFeeStrategist() != 0:
        s.setPerformanceFeeStrategist(0, {"from": dev})
    if s.withdrawalFee() != 0:
        s.setWithdrawalFee(0, {"from": dev})
    v.setGovernance(RECIPIENT, {"from": dev})
    s.setGovernance(RECIPIENT, {"from": dev})

  
    ## Verify balances
    assert v.totalSupply() == TO_MINT
    assert v.balanceOf(dev) == 0
    assert v.balanceOf(RECIPIENT) == TO_MINT

    ## Verify Basic stuff
    registry = BadgerRegistry.at(REGISTRY)

    governance = registry.get("governance")
    guardian = registry.get("guardian")
    keeper = registry.get("keeper")
    controller = "0x3F61344BA56df00dad9bBcA05d98CA2AeC43Ba0B" ## Restitution Controller
    badgerTree = registry.get("badgerTree")

    check_parameters(
            s, v, governance, guardian, keeper, controller, badgerTree
    )



def check_parameters(
    strategy, vault, governance, guardian, keeper, controller, badgerTree
):
    assert strategy.want() == WANT
    assert vault.token() == WANT

    assert strategy.controller() == controller
    assert vault.controller() == controller

    assert strategy.performanceFeeGovernance() == 0
    assert strategy.performanceFeeStrategist() == 0
    assert strategy.withdrawalFee() == 0

    assert strategy.keeper() == keeper
    assert vault.keeper() == keeper
    assert strategy.guardian() == guardian
    assert vault.guardian() == guardian
    assert strategy.strategist() == governance
    assert strategy.governance() == governance
    assert vault.governance() == governance

    # Not all strategies use the badgerTree
    try:
        if strategy.badgerTree() != AddressZero:
            assert strategy.badgerTree() == badgerTree
    except:
        pass

    console.print("[blue]All Parameters checked![/blue]")

def connect_account():
    click.echo(f"You are using the '{network.show_active()}' network")
    dev = accounts.load(click.prompt("Account", type=click.Choice(accounts.load())))
    click.echo(f"You are using: 'dev' [{dev.address}]")
    return dev
