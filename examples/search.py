"""
Example: Search publicly shared symphonies.

This example shows how to search the database of publicly shared symphonies
using various filters and sorting options.
"""

from composer import ComposerClient
import os
from dotenv import load_dotenv

load_dotenv()


def fmt_pct(val):
    """Format a value as percentage, or return N/A if None."""
    return f"{val:.2%}" if val is not None else "N/A"


def fmt_num(val, decimals=2):
    """Format a number with specified decimals, or return N/A if None."""
    return f"{val:.{decimals}f}" if val is not None else "N/A"


def main():
    client = ComposerClient(
        api_key=os.getenv("COMPOSER_API_KEY"),
        api_secret=os.getenv("COMPOSER_API_SECRET"),
    )

    print("=" * 60)
    print("SEARCH: TOP CUMULATIVE RETURNS")
    print("=" * 60)

    results = client.search.search_symphonies(
        order_by=[["oos_cumulative_return", "desc"]],
        offset=0,
    )

    print(f"Found {len(results)} symphonies\n")

    for i, symphony in enumerate(results[:5]):
        print(f"  {i + 1}. {symphony.name}")
        print(f"     ID: {symphony.symphony_sid}")
        print(f"     Backtest Days: {symphony.oos_num_backtest_days or 'N/A'}")
        print(f"     Cumulative Return: {fmt_pct(symphony.oos_cumulative_return)}")
        print(f"     Sharpe Ratio: {fmt_num(symphony.oos_sharpe_ratio)}")
        print(f"     Max Drawdown: {fmt_pct(symphony.oos_max_drawdown)}")
        print()

    print("=" * 60)
    print("SEARCH: BEAT SPY, LOWER RISK THAN BTC")
    print("=" * 60)
    print("Finding symphonies with returns > SPY and max drawdown < BTC...\n")

    where_clause = [
        "and",
        [">", "oos_annualized_rate_of_return", "oos_spy_annualized_rate_of_return"],
        ["<", "oos_max_drawdown", "oos_btcusd_max_drawdown"],
    ]
    results = client.search.search_symphonies(
        where=where_clause,
        order_by=[["oos_sharpe_ratio", "desc"]],
        offset=0,
    )

    print(f"Found {len(results)} symphonies\n")

    for i, symphony in enumerate(results[:5]):
        print(f"  {i + 1}. {symphony.name}")
        print(f"     Backtest Days: {symphony.oos_num_backtest_days or 'N/A'}")
        print(f"     Cumulative Return: {fmt_pct(symphony.oos_cumulative_return)}")
        print(f"     Sharpe Ratio: {fmt_num(symphony.oos_sharpe_ratio)}")
        print(f"     Max Drawdown: {fmt_pct(symphony.oos_max_drawdown)}")
        print(f"     SPY Alpha: {fmt_num(symphony.oos_spy_alpha)}")
        print()

    print("=" * 60)
    print("SEARCH: HIGH RETURNS, LOW DRAWDOWN, BEAT BENCHMARKS")
    print("=" * 60)
    print("Finding symphonies with >180 days backtest, >20% annualized,")
    print("returns > SPY, drawdown < BTC in both OOS and training...\n")

    where_clause = [
        "and",
        [">", "oos_num_backtest_days", 180],
        [
            ">",
            "oos_annualized_rate_of_return",
            ["*", 1.5, "oos_spy_annualized_rate_of_return"],
        ],
        [
            ">",
            "train_annualized_rate_of_return",
            ["*", 1.5, "train_spy_annualized_rate_of_return"],
        ],
        ["<", "oos_max_drawdown", ["*", 0.5, "oos_btcusd_max_drawdown"]],
        ["<", "train_max_drawdown", ["*", 0.5, "train_btcusd_max_drawdown"]],
        [">", "oos_annualized_rate_of_return", 0.2],
    ]
    results = client.search.search_symphonies(
        where=where_clause,
        order_by=[["oos_cumulative_return", "desc"]],
        offset=0,
    )

    print(f"Found {len(results)} symphonies\n")

    for i, symphony in enumerate(results[:5]):
        print(f"  {i + 1}. {symphony.name}")
        print(f"     Backtest Days: {symphony.oos_num_backtest_days or 'N/A'}")
        print(f"     Cumulative Return: {fmt_pct(symphony.oos_cumulative_return)}")
        print(f"     Sharpe Ratio: {fmt_num(symphony.oos_sharpe_ratio)}")
        print(f"     Max Drawdown: {fmt_pct(symphony.oos_max_drawdown)}")
        print(f"     SPY Alpha: {fmt_num(symphony.oos_spy_alpha)}")
        print()

    print("=" * 60)
    print("SEARCH: SMALL SYMPHONIES WITH GOOD PERFORMANCE")
    print("=" * 60)
    print("Finding symphonies with <10 IF+FILTER nodes and >0.5 Sharpe...\n")

    where_clause = [
        "and",
        ["<", ["+", "num_node_if", "num_node_filter"], 10],
        [">", "oos_sharpe_ratio", 0.5],
    ]
    results = client.search.search_symphonies(
        where=where_clause,
        order_by=[["oos_sharpe_ratio", "desc"]],
        offset=0,
    )

    print(f"Found {len(results)} symphonies\n")

    for i, symphony in enumerate(results[:5]):
        print(f"  {i + 1}. {symphony.name}")
        print(f"     IF Nodes: {symphony.num_node_if}")
        print(f"     Filter Nodes: {symphony.num_node_filter}")
        print(f"     Cumulative Return: {fmt_pct(symphony.oos_cumulative_return)}")
        print(f"     Sharpe Ratio: {fmt_num(symphony.oos_sharpe_ratio)}")
        print(f"     Max Drawdown: {fmt_pct(symphony.oos_max_drawdown)}")
        print()


if __name__ == "__main__":
    main()
