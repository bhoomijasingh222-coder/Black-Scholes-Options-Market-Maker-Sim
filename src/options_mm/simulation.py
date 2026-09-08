"""Market path, customer order flow, hedging, and P&L simulation."""

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .black_scholes import black_scholes
from .market_maker import MarketMaker


REGIMES = {
    "calm": {"volatility": 0.14, "adverse_risk": 0.10, "arrival_probability": 0.20},
    "volatile": {"volatility": 0.38, "adverse_risk": 0.35, "arrival_probability": 0.28},
    "adverse": {"volatility": 0.28, "adverse_risk": 0.85, "arrival_probability": 0.30},
}


@dataclass(frozen=True)
class SimulationConfig:
    regime: str = "calm"
    seed: int = 7
    steps: int = 500
    trading_days: float = 20.0
    initial_spot: float = 100.0
    strike: float = 100.0
    initial_expiry_years: float = 30.0 / 252.0
    rate: float = 0.03
    drift: float = 0.00
    contract_multiplier: int = 100
    hedge_transaction_cost_rate: float = 0.0002
    option_fee_per_contract: float = 0.02
    fill_sensitivity: float = 2.0

    def __post_init__(self) -> None:
        if self.regime not in REGIMES:
            raise ValueError(f"regime must be one of {sorted(REGIMES)}")
        if self.steps < 2 or self.trading_days <= 0:
            raise ValueError("steps must be >= 2 and trading_days must be positive")


def run_simulation(config: SimulationConfig, maker: MarketMaker | None = None) -> pd.DataFrame:
    maker = maker or MarketMaker()
    rng = np.random.default_rng(config.seed)
    regime = REGIMES[config.regime]
    sigma = regime["volatility"]
    adverse_risk = regime["adverse_risk"]
    dt = (config.trading_days / 252.0) / config.steps

    shocks = rng.standard_normal(config.steps)
    spots = np.empty(config.steps + 1)
    spots[0] = config.initial_spot
    for i, shock in enumerate(shocks):
        spots[i + 1] = spots[i] * np.exp((config.drift - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * shock)

    option_inventory = 0
    hedge_shares = 0.0
    cash = 0.0
    cumulative_cost = 0.0
    rows: list[dict[str, float | int | str]] = []

    for step in range(config.steps):
        spot = spots[step]
        next_spot = spots[step + 1]
        tau = max(config.initial_expiry_years - step * dt, 1e-8)
        bs = black_scholes(spot, config.strike, tau, config.rate, sigma, "call")
        quote = maker.quote(bs.price, sigma, option_inventory, adverse_risk)

        # Probability that a customer considers trading on each discrete step.
        base_probability = regime["arrival_probability"]
        bid_distance = max(bs.price - quote.bid, 0.0)
        ask_distance = max(quote.ask - bs.price, 0.0)
        p_sell_to_maker = base_probability * np.exp(-config.fill_sensitivity * bid_distance)
        p_buy_from_maker = base_probability * np.exp(-config.fill_sensitivity * ask_distance)

        # Informed customers are more likely to buy before an up move and sell before a down move.
        direction = np.sign(next_spot - spot)
        info_tilt = adverse_risk * 0.75
        p_buy_from_maker *= 1.0 + info_tilt * max(direction, 0.0)
        p_sell_to_maker *= 1.0 + info_tilt * max(-direction, 0.0)

        trade_size = 0  # +1 means maker buys; -1 means maker sells
        trade_price = np.nan
        u = rng.random()
        if u < min(p_sell_to_maker, 0.49) and option_inventory < maker.inventory_limit and quote.bid > 0:
            trade_size = 1
            trade_price = quote.bid
        elif u < min(p_sell_to_maker, 0.49) + min(p_buy_from_maker, 0.49) and option_inventory > -maker.inventory_limit and quote.ask < 1_000_000:
            trade_size = -1
            trade_price = quote.ask

        if trade_size:
            option_inventory += trade_size
            cash -= trade_size * trade_price * config.contract_multiplier
            fee = config.option_fee_per_contract * abs(trade_size)
            cash -= fee
            cumulative_cost += fee

        target_hedge = -option_inventory * bs.delta * config.contract_multiplier
        hedge_trade = target_hedge - hedge_shares
        hedge_cost = abs(hedge_trade) * spot * config.hedge_transaction_cost_rate
        cash -= hedge_trade * spot + hedge_cost
        hedge_shares = target_hedge
        cumulative_cost += hedge_cost

        pnl = cash + option_inventory * bs.price * config.contract_multiplier + hedge_shares * spot
        rows.append({
            "step": step,
            "regime": config.regime,
            "spot": spot,
            "time_to_expiry": tau,
            "fair_value": bs.price,
            "delta": bs.delta,
            "gamma": bs.gamma,
            "vega": bs.vega,
            "theta": bs.theta,
            "bid": quote.bid,
            "ask": quote.ask,
            "half_spread": quote.half_spread,
            "trade_size": trade_size,
            "trade_price": trade_price,
            "option_inventory": option_inventory,
            "hedge_shares": hedge_shares,
            "cash": cash,
            "cumulative_transaction_cost": cumulative_cost,
            "pnl": pnl,
        })

    # Liquidate at the final model value so runs are comparable and no risk remains hidden.
    final_spot = spots[-1]
    final_tau = max(config.initial_expiry_years - config.steps * dt, 1e-8)
    final_bs = black_scholes(final_spot, config.strike, final_tau, config.rate, sigma, "call")
    cash += option_inventory * final_bs.price * config.contract_multiplier + hedge_shares * final_spot
    close_cost = abs(hedge_shares) * final_spot * config.hedge_transaction_cost_rate
    cash -= close_cost
    cumulative_cost += close_cost
    rows[-1]["pnl"] = cash
    rows[-1]["cash"] = cash
    rows[-1]["cumulative_transaction_cost"] = cumulative_cost
    rows[-1]["option_inventory"] = 0
    rows[-1]["hedge_shares"] = 0.0
    return pd.DataFrame(rows)
