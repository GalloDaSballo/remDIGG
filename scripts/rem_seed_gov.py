from brownie import (
    accounts,
    network,
    BrikedStrategy,
    RemBadger,
    AdminUpgradeabilityProxy,
    Controller,
    BadgerRegistry,
    interface
)

from config import WANT, PROTECTED_TOKENS, FEES, REGISTRY

from helpers.constants import AddressZero

import click
from rich.console import Console

console = Console()

VAULT = "0x6aF7377b5009d7d154F36FE9e235aE1DA27Aea22"
STRATEGY = "0xD8d8aE4A5363edb6C3E01759576Da04bcc3a947e"
BADGER = "0x3472A5A71965499acd81997a54BBA8D852C6E53d"

TO_SEED = 6000e18 ## 600k shares with 18 decimals

GOV = "0xB65cef03b9B89f99517643226d76e286ee999e77" ## Dev Multi
WHALE = "0x4441776e6a5d61fa024a5117bfc26b953ad1f425"
def main():
  """ 
    Send funds to RemDIGG
    Verify share valiue changes as expected
  """


  v = RemBadger.at(VAULT)

  whale = accounts.at(WHALE, force=True)
  gov = accounts.at(GOV, force=True)

  badger = interface.IERC20(BADGER)
  badger.transfer(gov, TO_SEED, {"from": whale})

  assert v.getPricePerFullShare() == 0 ## 0 because shares but no balance

  badger.transfer(v, TO_SEED, {"from": gov})
  assert badger.balanceOf(v) == TO_SEED
  print(v.getPricePerFullShare())
  assert v.getPricePerFullShare() > 1e18 ## Increased
  assert v.getPricePerFullShare() == 1e18 * TO_SEED / 2000e18 ## exact math
