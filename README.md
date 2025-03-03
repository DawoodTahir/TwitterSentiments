# Vibe Checker

<div align="center">
  <img src="results.gif" alt="Demo GIF" width="600" />
</div>

## Overview
**Vibe Checker** is a Flask-based web application that analyzes the sentiment of tweets related to a specific keyword or topic. It uses the **Twitter API** to fetch tweets and the **OpenAI API** to perform sentiment analysis. The results are displayed in an easy-to-understand format, including sentiment distribution and engagement metrics.

## Features
- **Real-Time Sentiment Analysis**: Analyze the sentiment of tweets in real-time.
- **Engagement Metrics**: View likes, retweets, and replies for each tweet.
- **Interactive Results**: Visualize sentiment distribution and trends.
- **Customizable**: Enter any keyword or topic to analyze.

---

## How It Works
1. The user enters a keyword or topic of interest.
2. The app fetches recent tweets using the **Twitter API**.
3. Each tweet is analyzed for sentiment using the **OpenAI API**.
4. Results are displayed, including:
   - Sentiment distribution (positive, neutral, negative).
   - Engagement metrics (likes, retweets, replies).
   - A normalized sentiment score (0-100 scale).

---

## Setup Instructions

### Prerequisites
1. **Twitter API Access**:
   - Sign up for a [Twitter Developer Account](https://developer.twitter.com/).
   - Create an app and obtain your API keys (`API Key`, `API Secret Key`, `Access Token`, `Access Token Secret`).

2. **OpenAI API Access**:
   - Sign up for an [OpenAI API Key](https://platform.openai.com/).

3. **Python Environment**:
   - Ensure you have Python 3.7+ installed.

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/DawoodTahir/Vibe_Checker.git
   cd sentiment_analysis
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
    ```

3. Run the Flask app:
  ```bash
  flask run
  ```


4. To run the front end locally 
 ```bash
  cd frontend
  npm install
  npm run dev
  ```
   
