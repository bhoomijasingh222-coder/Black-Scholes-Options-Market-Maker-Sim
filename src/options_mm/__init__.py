"""Options pricing and market-making simulation package."""

from .black_scholes import OptionResult, black_scholes
from .simulation import SimulationConfig, run_simulation

__all__ = ["OptionResult", "black_scholes", "SimulationConfig", "run_simulation"]

