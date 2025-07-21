from newsapi import NewsApiClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import datetime

# Fetch recent news headlines for a given company symbol

def fetch_company_news(symbol, api_key, num_articles=10):
    newsapi = NewsApiClient(api_key=api_key)
    today = datetime.datetime.now().date()
    from_param = today - datetime.timedelta(days=7)
    query = f"{symbol} stock"
    all_articles = newsapi.get_everything(q=query,
                                          from_param=str(from_param),
                                          to=str(today),
                                          language='en',
                                          sort_by='relevancy',
                                          page_size=num_articles)
    headlines = [article['title'] for article in all_articles['articles']]
    return headlines

# Compute average sentiment score for a list of headlines

def compute_sentiment(headlines):
    analyzer = SentimentIntensityAnalyzer()
    scores = [analyzer.polarity_scores(h)['compound'] for h in headlines]
    if scores:
        avg_sentiment = sum(scores) / len(scores)
    else:
        avg_sentiment = 0
    return avg_sentiment
