import time
from datetime import datetime
from GoogleNews import GoogleNews
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from .sentiment_provider import SentimentProvider

class GoogleNewsProvider(SentimentProvider):
    """
    A sentiment provider that fetches news from Google News with a retry mechanism.
    """
    def __init__(self, fetch_delay: float = 1.5, max_retries: int = 4):
        """
        Initializes the provider.

        Args:
            fetch_delay (float): The base number of seconds to wait between requests.
            max_retries (int): The maximum number of times to retry a failed request.
        """
        self.google_news = GoogleNews(lang='en', encode='utf-8')
        self.analyzer = SentimentIntensityAnalyzer()
        self.fetch_delay = fetch_delay
        self.max_retries = max_retries

    def get_sentiment(self, symbol: str, date: str) -> float:
        """
        Fetches news for a symbol on a specific date and calculates the
        average sentiment of the headlines, with retries on failure.
        """
        # Convert date string to datetime object for date range
        target_date = datetime.strptime(date, '%Y-%m-%d')
        start_date = target_date.strftime('%m/%d/%Y')
        end_date = target_date.strftime('%m/%d/%Y')
        
        query = f"{symbol} stock"
        
        for attempt in range(self.max_retries):
            try:
                # Politeness delay before every attempt
                time.sleep(self.fetch_delay)
                
                self.google_news.clear()
                self.google_news.set_time_range(start_date, end_date)
                self.google_news.search(query)
                
                results = self.google_news.results()
                headlines = [res['title'] for res in results]
                
                if not headlines:
                    return 0.0

                scores = [self.analyzer.polarity_scores(h)['compound'] for h in headlines]
                return sum(scores) / len(scores) if scores else 0.0

            except Exception as e:
                # Check if it's a rate-limiting error
                if '429' in str(e):
                    backoff_time = (2 ** attempt) * 5  # Exponential backoff: 5s, 10s, 20s, 40s
                    print(f"\nRate limit hit for {date}. Retrying in {backoff_time} seconds... (Attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(backoff_time)
                else:
                    # It's a different, unexpected error
                    print(f"\nAn unexpected error occurred for {date}: {e}")
                    return 0.0 # Fail fast for other errors
        
        # If all retries have been exhausted
        print(f"\nFailed to fetch news for {date} after {self.max_retries} attempts due to persistent errors.")
        return 0.0 