import unittest

from options_mm.market_maker import MarketMaker
from options_mm.metrics import maximum_drawdown, performance_summary
from options_mm.simulation import SimulationConfig, run_simulation


class SimulationTests(unittest.TestCase):
    def test_seed_is_reproducible(self):
        config = SimulationConfig(seed=42, steps=100)
        first = run_simulation(config)
        second = run_simulation(config)
        self.assertTrue(first.equals(second))

    def test_inventory_limit_and_final_liquidation(self):
        result = run_simulation(SimulationConfig(regime="adverse", seed=2, steps=200))
        self.assertLessEqual(result["option_inventory"].abs().max(), 20)
        self.assertEqual(result["option_inventory"].iloc[-1], 0)
        self.assertEqual(result["hedge_shares"].iloc[-1], 0)

    def test_long_inventory_lowers_quotes(self):
        maker = MarketMaker()
        flat = maker.quote(5.0, 0.2, 0, 0.1)
        long = maker.quote(5.0, 0.2, 10, 0.1)
        self.assertLess(long.bid, flat.bid)
        self.assertLess(long.ask, flat.ask)

    def test_metrics_are_sensible(self):
        result = run_simulation(SimulationConfig(seed=8, steps=100))
        metrics = performance_summary(result)
        self.assertGreaterEqual(metrics["max_drawdown"], 0)
        self.assertGreaterEqual(metrics["transaction_costs"], 0)
        self.assertEqual(maximum_drawdown(result["pnl"]), metrics["max_drawdown"])


if __name__ == "__main__":
    unittest.main()

