from abc import ABC, abstractmethod

class SentimentProvider(ABC):
    """
    An abstract base class for all sentiment provider implementations.
    This ensures that any new provider we add will have a consistent interface.
    """
    @abstractmethod
    def get_sentiment(self, symbol: str, date: str):
        """
        Fetches news for a given symbol and date, and returns a sentiment score.

        Args:
            symbol (str): The stock ticker symbol.
            date (str): The target date in 'YYYY-MM-DD' format.

        Returns:
            float: The calculated sentiment score (e.g., between -1 and 1).
        """
        pass 