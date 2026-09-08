"""Black-Scholes pricing and analytical Greeks for European options."""

from dataclasses import dataclass
from math import erf, exp, log, pi, sqrt


def _normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))


def _normal_pdf(x: float) -> float:
    return exp(-0.5 * x * x) / sqrt(2.0 * pi)


@dataclass(frozen=True)
class OptionResult:
    price: float
    delta: float
    gamma: float
    vega: float
    theta: float
    rho: float


def black_scholes(
    spot: float,
    strike: float,
    time_to_expiry: float,
    rate: float,
    volatility: float,
    option_type: str = "call",
) -> OptionResult:
    """Return price and Greeks. Vega and rho are per 1.00 change; theta is per year."""
    if spot <= 0 or strike <= 0:
        raise ValueError("spot and strike must be positive")
    if time_to_expiry < 0 or volatility < 0:
        raise ValueError("time_to_expiry and volatility cannot be negative")
    if option_type not in {"call", "put"}:
        raise ValueError("option_type must be 'call' or 'put'")

    if time_to_expiry == 0:
        call_payoff = max(spot - strike, 0.0)
        put_payoff = max(strike - spot, 0.0)
        if option_type == "call":
            delta = 1.0 if spot > strike else (0.5 if spot == strike else 0.0)
            return OptionResult(call_payoff, delta, 0.0, 0.0, 0.0, 0.0)
        delta = -1.0 if spot < strike else (-0.5 if spot == strike else 0.0)
        return OptionResult(put_payoff, delta, 0.0, 0.0, 0.0, 0.0)

    if volatility == 0:
        discounted_strike = strike * exp(-rate * time_to_expiry)
        call = max(spot - discounted_strike, 0.0)
        put = max(discounted_strike - spot, 0.0)
        if option_type == "call":
            return OptionResult(call, float(spot > discounted_strike), 0.0, 0.0, 0.0, 0.0)
        return OptionResult(put, -float(spot < discounted_strike), 0.0, 0.0, 0.0, 0.0)

    root_t = sqrt(time_to_expiry)
    d1 = (log(spot / strike) + (rate + 0.5 * volatility**2) * time_to_expiry) / (volatility * root_t)
    d2 = d1 - volatility * root_t
    discount = exp(-rate * time_to_expiry)
    pdf_d1 = _normal_pdf(d1)
    gamma = pdf_d1 / (spot * volatility * root_t)
    vega = spot * pdf_d1 * root_t

    if option_type == "call":
        price = spot * _normal_cdf(d1) - strike * discount * _normal_cdf(d2)
        delta = _normal_cdf(d1)
        theta = -(spot * pdf_d1 * volatility) / (2 * root_t) - rate * strike * discount * _normal_cdf(d2)
        rho = strike * time_to_expiry * discount * _normal_cdf(d2)
    else:
        price = strike * discount * _normal_cdf(-d2) - spot * _normal_cdf(-d1)
        delta = _normal_cdf(d1) - 1.0
        theta = -(spot * pdf_d1 * volatility) / (2 * root_t) + rate * strike * discount * _normal_cdf(-d2)
        rho = -strike * time_to_expiry * discount * _normal_cdf(-d2)

    return OptionResult(price, delta, gamma, vega, theta, rho)

