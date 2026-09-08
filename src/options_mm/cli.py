"""Command-line runner for all market regimes."""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from .metrics import performance_summary
from .simulation import REGIMES, SimulationConfig, run_simulation


def run_experiment(output_dir: Path, seeds: list[int]) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    summaries = []
    representative = []
    for regime in REGIMES:
        for seed in seeds:
            result = run_simulation(SimulationConfig(regime=regime, seed=seed))
            summary = performance_summary(result)
            summary.update({"regime": regime, "seed": seed})
            summaries.append(summary)
            if seed == seeds[0]:
                result.to_csv(output_dir / f"simulation_{regime}.csv", index=False)
                representative.append(result)

    raw = pd.DataFrame(summaries)
    raw.to_csv(output_dir / "run_summaries.csv", index=False)
    grouped = raw.groupby("regime").agg(
        mean_pnl=("final_pnl", "mean"),
        pnl_std=("final_pnl", "std"),
        mean_max_drawdown=("max_drawdown", "mean"),
        mean_trades=("trades", "mean"),
        mean_costs=("transaction_costs", "mean"),
        worst_inventory=("max_abs_inventory", "max"),
    ).reset_index()
    grouped.to_csv(output_dir / "regime_summary.csv", index=False)

    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    for result in representative:
        label = str(result["regime"].iloc[0])
        axes[0].plot(result["step"], result["pnl"], label=label)
        axes[1].plot(result["step"], result["option_inventory"], label=label)
    axes[0].set_ylabel("Marked-to-market P&L ($)")
    axes[1].set_ylabel("Option inventory")
    axes[1].set_xlabel("Simulation step")
    axes[0].legend()
    axes[0].grid(alpha=0.25)
    axes[1].grid(alpha=0.25)
    fig.suptitle("Options market maker: representative seeded runs")
    fig.tight_layout()
    fig.savefig(output_dir / "performance.png", dpi=180)
    plt.close(fig)
    return grouped


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the options market-making experiment")
    parser.add_argument("--output", type=Path, default=Path("outputs"))
    parser.add_argument("--runs", type=int, default=50, help="number of seeds per regime")
    args = parser.parse_args()
    summary = run_experiment(args.output, list(range(1, args.runs + 1)))
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()

