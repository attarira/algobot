import click
from data_fetcher.market_data import fetch_historical_data
from strategies.sma_crossover import SMACrossoverStrategy
from strategies.sentiment_strategy import SentimentSMACrossoverStrategy
from data_fetcher.google_news_provider import GoogleNewsProvider
from broker.sandbox_broker import SandboxBroker
from backtesting.backtest_engine import BacktestEngine

@click.group()
def cli():
    pass

@cli.command()
@click.option('--symbol', default='AAPL', help='Asset symbol to trade')
@click.option('--capital', default=10000, type=float, help='Starting capital (USD)')
@click.option('--short_window', default=20, type=int, help='Short-term SMA window')
@click.option('--long_window', default=50, type=int, help='Long-term SMA window')
@click.option('--sentiment', is_flag=True, help='Enable sentiment analysis for the backtest.')
@click.option('--period', default='1y', help='Data period for backtest (e.g., "6mo", "1y").')
def backtest(symbol, capital, short_window, long_window, sentiment, period):
    """Run a backtest of the trading strategy."""
    print(f"Running backtest for {symbol} over the last {period}...")
    data = fetch_historical_data(symbol, period=period)

    if sentiment:
        print("Using Sentiment-Aware SMA Crossover Strategy with Google News.")
        sentiment_provider = GoogleNewsProvider()
        strategy = SentimentSMACrossoverStrategy(short_window, long_window, sentiment_provider)
        engine = BacktestEngine(data, strategy, starting_capital=capital, symbol_for_strategy=symbol)
    else:
        print("Using basic SMA Crossover Strategy.")
        strategy = SMACrossoverStrategy(short_window, long_window)
        engine = BacktestEngine(data, strategy, starting_capital=capital)
    
    portfolio_history = engine.run()
    metrics = engine.calculate_metrics(portfolio_history)
    
    print("\n--- Backtest Results ---")
    for key, value in metrics.items():
        print(f"{key}: {value}")
    print("------------------------\n")

@cli.command()
@click.option('--symbol', default='AAPL', help='Asset symbol to trade')
@click.option('--capital', default=10000, type=float, help='Starting capital (USD)')
@click.option('--short_window', default=20, type=int, help='Short-term SMA window')
@click.option('--long_window', default=50, type=int, help='Long-term SMA window')
@click.option('--stop_loss_pct', default=0.03, type=float, help='Stop-loss percentage (e.g., 0.03 for 3%)')
@click.option('--momentum_window', default=3, type=int, help='Momentum window (days)')
@click.option('--momentum_threshold', default=0.01, type=float, help='Momentum threshold (e.g., 0.01 for 1%)')
def trade(symbol, capital, short_window, long_window, stop_loss_pct, momentum_window, momentum_threshold):
    """Run the bot in paper trading mode (sentiment disabled for now)."""
    print("Paper trading mode is currently running without live sentiment.")
    data = fetch_historical_data(symbol, period='6mo')
    from strategies.aggressive_sma_crossover import AggressiveSMACrossoverStrategy
    strategy = AggressiveSMACrossoverStrategy(
        short_window, long_window,
        stop_loss_pct=stop_loss_pct,
        momentum_window=momentum_window,
        momentum_threshold=momentum_threshold
    )
    engine = BacktestEngine(data, strategy, starting_capital=capital)
    portfolio_history = engine.run()
    metrics = engine.calculate_metrics(portfolio_history)
    print("\n--- Paper Trading Results ---")
    for key, value in metrics.items():
        print(f"{key}: {value}")
    print("------------------------\n")

if __name__ == '__main__':
    cli()