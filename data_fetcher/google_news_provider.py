import time
from datetime import datetime
from GoogleNews import GoogleNews
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from .sentiment_provider import SentimentProvider

class GoogleNewsProvider(SentimentProvider):
    """
    A sentiment provider that fetches news from Google News.
    """
    def __init__(self, fetch_delay: float = 1.0):
        """
        Initializes the provider.

        Args:
            fetch_delay (float): The number of seconds to wait between requests
                                 to avoid being rate-limited.
        """
        self.google_news = GoogleNews(lang='en', encode='utf-8')
        self.analyzer = SentimentIntensityAnalyzer()
        self.fetch_delay = fetch_delay

    def get_sentiment(self, symbol: str, date: str) -> float:
        """
        Fetches news for a symbol on a specific date and calculates the
        average sentiment of the headlines.
        """
        # Be respectful of Google's servers
        time.sleep(self.fetch_delay)

        # Convert date string to datetime object for date range
        target_date = datetime.strptime(date, '%Y-%m-%d')
        start_date = target_date.strftime('%m/%d/%Y')
        end_date = target_date.strftime('%m/%d/%Y')
        
        query = f"{symbol} stock"
        
        try:
            self.google_news.clear() # Clear previous results
            self.google_news.set_time_range(start_date, end_date)
            self.google_news.search(query)
            
            results = self.google_news.results()
            headlines = [res['title'] for res in results]
            
            if not headlines:
                return 0.0

            scores = [self.analyzer.polarity_scores(h)['compound'] for h in headlines]
            return sum(scores) / len(scores) if scores else 0.0

        except Exception as e:
            print(f"An error occurred while fetching news for {symbol} on {date}: {e}")
            return 0.0 