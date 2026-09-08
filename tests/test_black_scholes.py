import math
import unittest

from options_mm.black_scholes import black_scholes


class BlackScholesTests(unittest.TestCase):
    def test_known_at_the_money_call(self):
        result = black_scholes(100, 100, 1, 0.05, 0.20, "call")
        self.assertAlmostEqual(result.price, 10.4506, places=3)
        self.assertAlmostEqual(result.delta, 0.6368, places=3)

    def test_put_call_parity(self):
        call = black_scholes(100, 95, 0.5, 0.03, 0.25, "call")
        put = black_scholes(100, 95, 0.5, 0.03, 0.25, "put")
        lhs = call.price - put.price
        rhs = 100 - 95 * math.exp(-0.03 * 0.5)
        self.assertAlmostEqual(lhs, rhs, places=10)

    def test_expiry_payoff(self):
        self.assertEqual(black_scholes(110, 100, 0, 0.03, 0.2).price, 10)
        self.assertEqual(black_scholes(90, 100, 0, 0.03, 0.2, "put").price, 10)


if __name__ == "__main__":
    unittest.main()

