"""Performance and risk metrics."""

import numpy as np
import pandas as pd


def maximum_drawdown(pnl: pd.Series) -> float:
    running_peak = pnl.cummax()
    return float((running_peak - pnl).max())


def performance_summary(results: pd.DataFrame) -> dict[str, float]:
    changes = results["pnl"].diff().dropna()
    std = float(changes.std(ddof=1)) if len(changes) > 1 else 0.0
    sharpe_like = float(changes.mean() / std * np.sqrt(len(changes))) if std > 0 else 0.0
    return {
        "final_pnl": float(results["pnl"].iloc[-1]),
        "max_drawdown": maximum_drawdown(results["pnl"]),
        "pnl_volatility": std,
        "sharpe_like": sharpe_like,
        "trades": int(results["trade_size"].abs().sum()),
        "max_abs_inventory": int(results["option_inventory"].abs().max()),
        "transaction_costs": float(results["cumulative_transaction_cost"].iloc[-1]),
        "average_half_spread": float(results["half_spread"].mean()),
    }

