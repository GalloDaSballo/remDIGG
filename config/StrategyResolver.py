from brownie import interface
from helpers.StrategyCoreResolver import StrategyCoreResolver
from rich.console import Console

console = Console()


class StrategyResolver(StrategyCoreResolver):
    def get_strategy_destinations(self):
        """
        Track balances for all strategy implementations
        (Strategy Must Implement)
        """
        return {
        }

    def hook_after_confirm_withdraw(self, before, after, params):
        """
        Specifies extra check for ordinary operation on withdrawal
        Use this to verify that balances in the get_strategy_destinations are properly set
        """
        ## Check that balance in gauge goes down
        before.balances("want", "strategy") > after.balances("want", "strategy")

    def hook_after_confirm_deposit(self, before, after, params):
        """
        Specifies extra check for ordinary operation on deposit
        Use this to verify that balances in the get_strategy_destinations are properly set
        """
        ## Check that balance in gauge goes up
        after.balances("want", "strategy") > before.balances("want", "strategy")

    def hook_after_earn(self, before, after, params):
        """
        Specifies extra check for ordinary operation on earn
        Use this to verify that balances in the get_strategy_destinations are properly set
        """
        ## Check that balance in gauge goes up
        after.balances("want", "strategy") > before.balances("want", "strategy")

    def confirm_harvest(self, before, after, tx):
        """
        Verfies that the Harvest produced yield and fees
        """
        console.print("=== Compare Harvest ===")
        self.manager.printCompare(before, after)
        self.confirm_harvest_state(before, after, tx)

        valueGained = after.get("sett.pricePerFullShare") == before.get(
            "sett.pricePerFullShare"
        )

        # assert valueGained ## NO value gained

    def confirm_tend(self, before, after, tx):
        """
        Tend Should;
        - Increase the number of staked tended tokens in the strategy-specific mechanism
        - Reduce the number of tended tokens in the Strategy to zero

        (Strategy Must Implement)
        """
        console.print("=== Compare Tend ===")
        self.manager.printCompare(before, after)


        # # assert after.get("strategy.balanceOfWant") == before.get(
        #         "strategy.balanceOfWant"
        # )

        # # assert after.get("strategy.balanceOfPool") == before.get(
        #         "strategy.balanceOfPool"
        # )
            
