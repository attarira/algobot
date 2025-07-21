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
# For now, we focus on the backtesting workflow.
def trade(symbol, capital, short_window, long_window):
    """Run the bot in paper trading mode (sentiment disabled for now)."""
    print("Paper trading mode is currently running without live sentiment.")
    # This part needs to be refactored to use the new provider structure as well.
    # We can tackle this next.
    pass

if __name__ == '__main__':
    cli() 