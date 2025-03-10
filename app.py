import os
import requests
import time
from flask import Flask, render_template, request, jsonify
import datetime
import matplotlib
import matplotlib.pyplot as plt
import io
import base64
import re
from openai import OpenAI
from flask_cors import cross_origin
from flask_cors import CORS
# Set Matplotlib to a non-GUI backend
matplotlib.use('Agg')

# Load API keys from environment variables
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Flask app setup
app = Flask(__name__)
# ✅ Allow CORS for Local & Deployed Frontend
CORS(app, resources={r"/*": {"origins": [
    "http://localhost:5173", 
    "https://sentiment-analysis-ui.netlify.app"
]}})

# Headers for Twitter API authentication
HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "User-Agent": "v2TweetSearch"
}
SEARCH_URL = "https://api.twitter.com/2/tweets/search/recent"

class TwitterAPI:
    """Handles fetching tweets from Twitter API."""
    
    def __init__(self):
        self.search_url = SEARCH_URL
        self.headers = HEADERS

    def search_tweets(self, keyword: str, count: int = 50):
        """Fetch tweets containing a specific keyword along with reactions."""
        try:
            params = {
                "query": keyword,
                "max_results": min(count, 100),
                "tweet.fields": "created_at,public_metrics,text",
            }

            response = requests.get(self.search_url, headers=self.headers, params=params)

            if response.status_code != 200:
                raise Exception(f"Request Error: {response.status_code} {response.text}")

            return response.json().get("data", [])
        except Exception as e:
            print(f"Error fetching tweets: {e}")
            return []

class SentimentAnalyzer:
    """Uses OpenAI API to analyze sentiment of tweets."""
    
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def analyze_batch(self, tweets):
        """Analyzes sentiment of tweets in batches."""
        batch_size = 10
        results = []
        
        for i in range(0, len(tweets), batch_size):
            batch = tweets[i:i + batch_size]
            response = self._get_sentiment(batch)
            results.extend(response)
            time.sleep(1) 
        
        return results

    def _get_sentiment(self, tweets):
        """Calls OpenAI API to classify tweets as Positive, Neutral, or Negative."""
        prompt = "Analyze the sentiment of each tweet below. Respond with only 'Positive', 'Neutral,' or 'Negative'."
        prompt += "\n".join([f"- {tweet}" for tweet in tweets])

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100
            )
            return [line.strip().capitalize() for line in response.choices[0].message.content.split("\n") if line]
        except Exception as e:
            print(f"Error with OpenAI API: {e}")
            return ["Error"] * len(tweets)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    keyword = request.form.get("keyword")
    
    
    # Extract only alphanumeric characters (letters and numbers) from the keyword
    if keyword:
        # Use regex to remove all non-alphanumeric characters
        keyword = re.sub(r"[^a-zA-Z0-9]", "", keyword)
    else:
        return jsonify({"error": "Keyword is required."})
    twitter_api = TwitterAPI()
    sentiment_analyzer = SentimentAnalyzer()
    
    tweets = twitter_api.search_tweets(keyword, 1000)
    if not tweets:
        return jsonify({"error": "No tweets found."})
    
    tweet_texts = [tweet["text"] for tweet in tweets]
    tweet_dates = [tweet["created_at"] for tweet in tweets] 
    engagement_metrics = [tweet["public_metrics"] for tweet in tweets]
    sentiments = sentiment_analyzer.analyze_batch(tweet_texts)
    print(sentiments)

    sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
    for sentiment in sentiments:
        sentiment= sentiment.split('-')[-1].strip()
        if sentiment in sentiment_counts:
            sentiment_counts[sentiment] += 1
    
    total_tweets = sum(sentiment_counts.values())

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
    normalized_sentiment=0.5 * normalized_sentiment
    engagement_score = 0.3 * engagement_score
    activity_score = 0.2 * activity_score
    vibe_score = normalized_sentiment + engagement_score + activity_score
    vibe_score = max(0, min(vibe_score, 100))  # Ensure within 0-100
    return jsonify({

        "tweets": list(zip(sentiments, tweet_texts)),
        "sentiment_counts": sentiment_counts,
        "vibe_score" : vibe_score,
        "normalized_sentiment" : normalized_sentiment,        
        "engagement_score" : engagement_score,
        "activity_score" : activity_score
    })
import datetime

STATIC_FOLDER = "static"
if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)

# Function to delete old files
def cleanup_old_files():
    now = time.time()
    for filename in os.listdir(STATIC_FOLDER):
        file_path = os.path.join(STATIC_FOLDER, filename)
        if os.path.isfile(file_path):
            file_age = now - os.path.getmtime(file_path)
            if file_age > 86400:  # 24 hours
                os.remove(file_path)

@app.route("/graphs", methods=["POST"])
def generate_graphs():
    cleanup_old_files()
    data = request.get_json()
    sentiment_counts = data.get("sentiment_counts", {})
    vibe_score=data.get("vibe_score",{})
    

    return jsonify({
        None
    })



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use PORT from Render, fallback to 5000
    app.run(host="0.0.0.0", port=port, debug=False)