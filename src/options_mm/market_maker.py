"""Inventory-aware option quote generation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Quote:
    bid: float
    ask: float
    reservation_price: float
    half_spread: float


@dataclass
class MarketMaker:
    base_half_spread: float = 0.08
    volatility_spread_factor: float = 0.35
    adverse_selection_factor: float = 0.18
    inventory_skew: float = 0.025
    inventory_limit: int = 20

    def quote(self, fair_value: float, volatility: float, inventory: int, adverse_risk: float) -> Quote:
        """Lower quotes when long and raise them when short to encourage inventory reduction."""
        risk_scale = max(fair_value, 0.50)
        half_spread = self.base_half_spread + risk_scale * (
            self.volatility_spread_factor * volatility + self.adverse_selection_factor * adverse_risk
        )
        reservation = fair_value - self.inventory_skew * inventory
        bid = max(0.0, reservation - half_spread)
        ask = max(bid + 0.01, reservation + half_spread)

        if inventory >= self.inventory_limit:
            bid = 0.0  # refuse to buy more options
        if inventory <= -self.inventory_limit:
            ask = max(ask, 1_000_000.0)  # refuse to sell more options
        return Quote(bid, ask, reservation, half_spread)

