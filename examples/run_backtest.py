from composer import ComposerClient, BacktestParams

# Initialize client with your API credentials
client = ComposerClient(api_key="your-api-key", api_secret="your-api-secret")

# Run backtest with QQQ as benchmark
result = client.symphony.backtest_symphony_by_id(
    "VPVpD1SoqR5ykVu4NdWS", params=BacktestParams(benchmark_tickers=["QQQ"])
)

print(f"Symphony Sharpe Ratio: {result.stats.sharpe_ratio:.2f}")
print(f"QQQ Sharpe Ratio: {result.stats.benchmarks['QQQ'].sharpe_ratio:.2f}")
