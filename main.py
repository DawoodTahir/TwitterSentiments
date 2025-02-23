# import requests
# import os


# # Load Bearer Token from environment variable
# BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
# #Headers for authentication
# headers = {
#     "Authorization": f"Bearer {BEARER_TOKEN}",
#     "User-Agent": "v2TweetSearch"
# }
# # Twitter API v2 endpoint for searching recent tweets
# SEARCH_URL = "https://api.twitter.com/2/tweets/search/recent"



# class TwitterAPI:
#     def __init__(self):
#         self.SEARCH_URL=SEARCH_URL
#         self.headers = headers



# # Function to search for tweets
#     def search_tweets(self,keyword,count=50):

#         try:
#             # Parameters for the search query
#             params = {
#                 "query": keyword,  # The keyword to search for
#                 "max_results": count,  # Number of tweets to retrieve (max 100)
#                 "tweet.fields": "created_at,public_metrics,text",  # Get extra fields
#             }

#             # Make the request to the Twitter API
#             response = requests.get(self.SEARCH_URL, headers=self.headers, params=params)

#             # Check if the request was successful
#             if response.status_code != 200:
#                 raise Exception(f"Request returned an error: {response.status_code} {response.text}")

#             # Parse the JSON response
#             json_response = response.json()

#             # Print tweet details
#             for tweet in json_response.get("data", []):
#                 print(f"Tweet: {tweet['text']}")
#                 print(f"Created at: {tweet['created_at']}")
#                 print(f"Likes: {tweet['public_metrics']['like_count']}")
#                 print(f"Retweets: {tweet['public_metrics']['retweet_count']}")
#                 print("-" * 40)

#         except Exception as e:
#             print(f"Error: {e}")

# # Example usage
# if __name__ == "__main__":
#     keyword = "DoGeCoin"  # Replace with your desired keyword
#     TwitterAPI.search_tweets(keyword, count=10)  # Search for 10 tweets
import os
import requests
import time
from typing import List, Dict
from openai import OpenAI
import datetime

# Load API keys from environment variables
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Headers for Twitter API authentication
HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "User-Agent": "v2TweetSearch"
}

# Twitter API v2 endpoint for searching recent tweets
SEARCH_URL = "https://api.twitter.com/2/tweets/search/recent"

class TwitterAPI:
    """Handles fetching tweets from Twitter API using requests."""
    
    def __init__(self):
        self.search_url = SEARCH_URL
        self.headers = HEADERS

    def search_tweets(self, keyword: str, count: int = 50) -> List[Dict]:
        """Fetch tweets containing a specific keyword along with reactions."""
        try:
            params = {
                "query": keyword,
                "max_results": min(count, 100),  # Max 100 per request
                "tweet.fields": "created_at,public_metrics,text",
            }

            response = requests.get(self.search_url, headers=self.headers, params=params)

            if response.status_code != 200:
                raise Exception(f"Request Error: {response.status_code} {response.text}")

            tweets_data = response.json().get("data", [])
            return tweets_data  # Return full tweet objects
        except Exception as e:
            print(f"Error fetching tweets: {e}")
            return []

class SentimentAnalyzer:
    """Uses OpenAI API to analyze sentiment of tweets."""
    
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def analyze_batch(self, tweets: List[str]) -> List[str]:
        """Analyzes sentiment of tweets in batches to optimize API calls."""
        batch_size = 10  # Process tweets in batches of 10
        results = []
        
        for i in range(0, len(tweets), batch_size):
            batch = tweets[i:i + batch_size]
            response = self._get_sentiment(batch)
            results.extend(response)
            time.sleep(1)  # Avoid exceeding API rate limits
        
        return results

    def _get_sentiment(self, tweets: List[str]) -> List[str]:
        """Calls OpenAI API to classify tweets as Positive, Neutral, or Negative."""
        prompt = "Analyze the sentiment of each tweet below. Respond with only 'Positive', 'Neutral,' or 'Negative' for each tweet. Do not include any explanations or extra text."
        prompt += "\n".join([f"- {tweet}" for tweet in tweets])

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100
            )
            analysis = response.choices[0].message.content.split("\n")
            return [line.strip() for line in analysis if line]
        except Exception as e:
            print(f"Error with OpenAI API: {e}")
            return ["Error"] * len(tweets)

class TweetSentimentAnalyzer:
    """Fetches tweets using Twitter API and analyzes sentiment using OpenAI."""

    def __init__(self):
        self.twitter_api = TwitterAPI()
        self.sentiment_analyzer = SentimentAnalyzer()

    def analyze_keyword(self, keyword: str, max_tweets: int = 50):
        """Fetches tweets, analyzes sentiment, extracts engagement, and calculates vibe score."""
        tweets = self.twitter_api.search_tweets(keyword, max_tweets)
        
        if not tweets:
            print("No tweets found.")
            return
        
        tweet_texts = [tweet["text"] for tweet in tweets]
        tweet_dates = [tweet["created_at"] for tweet in tweets]
        engagement_metrics = [tweet["public_metrics"] for tweet in tweets]

        # Analyze sentiments
        sentiments = self.sentiment_analyzer.analyze_batch(tweet_texts)
        
        # Improved sentiment counting using case-insensitive matching
        sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
        for sentiment in sentiments:
            s = sentiment.lower()
            if "positive" in s:
                sentiment_counts["positive"] += 1
            elif "negative" in s:
                sentiment_counts["negative"] += 1
            elif "neutral" in s:
                sentiment_counts["neutral"] += 1

        total_tweets = sum(sentiment_counts.values())
        if total_tweets == 0:
            print("No valid sentiment data.")
            return

        # Calculate percentages for display
        positive_pct = (sentiment_counts["positive"] / total_tweets) * 100
        neutral_pct = (sentiment_counts["neutral"] / total_tweets) * 100
        negative_pct = (sentiment_counts["negative"] / total_tweets) * 100

        # Professional Sentiment Normalization:
        # Calculate a normalized sentiment index from -1 (all negative) to +1 (all positive)
        sentiment_value = (sentiment_counts["positive"] - sentiment_counts["negative"]) / total_tweets
        # Normalize to a 0-100 scale: 50 is neutral, above 50 positive, below 50 negative
        normalized_sentiment = ((sentiment_value + 1) / 2) * 100

        # Calculate Engagement Score
        total_likes = sum(t["like_count"] for t in engagement_metrics)
        total_retweets = sum(t["retweet_count"] for t in engagement_metrics)
        total_replies = sum(t["reply_count"] for t in engagement_metrics)
        total_quotes = sum(t["quote_count"] for t in engagement_metrics)

        engagement_score = (total_likes + total_retweets * 2 + total_replies * 1.5 + total_quotes * 1.2) / total_tweets
        engagement_score = min(engagement_score, 100)  # Cap at 100

        # Calculate Activity Score (tweets per day)
        oldest_tweet_date = min(tweet_dates) if tweet_dates else None
        if oldest_tweet_date:
            oldest_date = datetime.datetime.strptime(oldest_tweet_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            days_span = (datetime.datetime.utcnow() - oldest_date).days + 1
            activity_score = min((total_tweets / days_span) * 10, 100)  # Normalize to 100
        else:
            activity_score = 0

        # Professional Vibe Score Computation:
        # Using weighted aggregation:
        #  - 50% weight for normalized sentiment
        #  - 30% weight for engagement
        #  - 20% weight for activity
        vibe_score = 0.5 * normalized_sentiment + 0.3 * engagement_score + 0.2 * activity_score
        vibe_score = max(0, min(vibe_score, 100))  # Ensure within 0-100

        # Print Report
        print(f"\n🔹 Keyword: {keyword}")
        print(f"📊 Sentiment Breakdown:")
        print(f"   - Positive: {positive_pct:.2f}%")
        print(f"   - Neutral: {neutral_pct:.2f}%")
        print(f"   - Negative: {negative_pct:.2f}%")
        print(f"   - Normalized Sentiment Index: {normalized_sentiment:.2f}/100")
        print(f"🔥 Engagement Score: {engagement_score:.2f}/100")
        print(f"📈 Activity Score: {activity_score:.2f}/100")
        print(f"🌟 **Vibe Score**: {vibe_score:.2f}/100")

        for tweet, sentiment in zip(tweet_texts, sentiments):
            print(f"\nTweet: {tweet}\nSentiment: {sentiment}\n{'-'*40}")

# Example Usage
if __name__ == "__main__":
    analyzer = TweetSentimentAnalyzer()
    analyzer.analyze_keyword("BabarAzam", max_tweets=50)

