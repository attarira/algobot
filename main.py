import click
from data_fetcher.market_data import fetch_historical_data
from strategies.sma_crossover import SMACrossoverStrategy
from broker.sandbox_broker import SandboxBroker
from data_fetcher.news_sentiment import fetch_company_news, compute_sentiment

@click.command()
@click.option('--symbol', default='TSLA', help='Asset symbol to trade')
@click.option('--capital', default=10000, type=float, help='Starting capital (USD)')
@click.option('--short_window', default=20, type=int, help='Short-term SMA window')
@click.option('--long_window', default=50, type=int, help='Long-term SMA window')
@click.option('--newsapi-key', prompt=True, hide_input=True, help='NewsAPI key for fetching news')
def run_bot(symbol, capital, short_window, long_window, newsapi_key):
    print(f"Starting trading bot for {symbol} with ${capital} capital...")
    data = fetch_historical_data(symbol)
    # Fetch news and compute sentiment
    headlines = fetch_company_news(symbol, newsapi_key)
    sentiment = compute_sentiment(headlines)
    print(f"News sentiment for {symbol}: {sentiment:.2f}")
    broker = SandboxBroker(starting_capital=capital)
    strategy = SMACrossoverStrategy(short_window, long_window)
    signals = strategy.generate_signals(data)
    # Only allow buys if sentiment > 0
    signals['sentiment'] = sentiment
    signals['signal'] = signals.apply(lambda row: row['signal'] if row['sentiment'] > 0 else 0, axis=1)
    signals['positions'] = signals['signal'].diff().fillna(0)
    broker.run_paper_trading(data, signals)

if __name__ == '__main__':
    run_bot() 