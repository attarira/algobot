import click
from data_fetcher.market_data import fetch_historical_data
from strategies.sma_crossover import SMACrossoverStrategy
from broker.sandbox_broker import SandboxBroker

@click.command()
@click.option('--symbol', default='AAPL', help='Asset symbol to trade')
@click.option('--capital', default=10000, type=float, help='Starting capital (USD)')
@click.option('--short_window', default=20, type=int, help='Short-term SMA window')
@click.option('--long_window', default=50, type=int, help='Long-term SMA window')
def run_bot(symbol, capital, short_window, long_window):
    print(f"Starting trading bot for {symbol} with ${capital} capital...")
    data = fetch_historical_data(symbol)
    broker = SandboxBroker(starting_capital=capital)
    strategy = SMACrossoverStrategy(short_window, long_window)
    signals = strategy.generate_signals(data)
    broker.run_paper_trading(data, signals)

if __name__ == '__main__':
    run_bot() 