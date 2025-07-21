import pandas as pd
from tqdm import tqdm
from .sma_crossover import SMACrossoverStrategy
from data_fetcher.sentiment_provider import SentimentProvider

class SentimentSMACrossoverStrategy(SMACrossoverStrategy):
    def __init__(self, short_window: int, long_window: int, sentiment_provider: SentimentProvider):
        super().__init__(short_window, long_window)
        if not isinstance(sentiment_provider, SentimentProvider):
            raise TypeError("sentiment_provider must be an instance of SentimentProvider")
        self.sentiment_provider = sentiment_provider

    def generate_signals(self, data: pd.DataFrame, symbol: str) -> pd.DataFrame:
        # First, get the basic SMA signals
        signals = super().generate_signals(data)
        
        # Now, apply sentiment analysis day-by-day
        print("Applying sentiment analysis to historical data (this may take a while)...")
        
        # Use tqdm for a progress bar
        for date in tqdm(signals.index, desc="Analyzing Sentiment"):
            # Get sentiment from the provider
            sentiment = self.sentiment_provider.get_sentiment(symbol, date.strftime('%Y-%m-%d'))
            
            # If sentiment is not positive, cancel any buy signals for that day
            if sentiment <= 0 and signals.loc[date, 'positions'] == 1:
                signals.loc[date, 'positions'] = 0 # Cancel the buy
        
        return signals 