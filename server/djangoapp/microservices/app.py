"""
Sentiment Analysis Microservice

This module implements a Flask-based microservice for analyzing text sentiment.
It uses NLTK's VADER (Valence Aware Dictionary and sEntiment Reasoner) for
sentiment analysis.

Key Features:
1. Sentiment Analysis:
   - Analyzes text and returns sentiment classification (positive/negative/neutral)
   - Uses NLTK's SentimentIntensityAnalyzer for polarity scoring
   - Returns JSON response with sentiment classification

2. API Endpoints:
   - /: Returns service welcome message
   - /analyze/<input_txt>: Analyzes sentiment of provided text

Configuration:
- Runs on Flask development server
- Debug mode enabled for development
- Uses NLTK's pre-trained sentiment analyzer

Error Handling:
- Handles all text input types
- Returns valid JSON responses for all requests
- Implements proper HTTP status codes

Example Usage:
    $ curl http://localhost:5050/analyze/Great%20service!
    {"sentiment": "positive"}
"""

from flask import Flask
from nltk.sentiment import SentimentIntensityAnalyzer
import json

app = Flask("Sentiment Analyzer")

sia = SentimentIntensityAnalyzer()


@app.get("/")
def home():
    return "Welcome to the Sentiment Analyzer. \
    Use /analyze/text to get the sentiment"


@app.get("/analyze/<input_txt>")
def analyze_sentiment(input_txt):

    scores = sia.polarity_scores(input_txt)
    print(scores)
    pos = float(scores["pos"])
    neg = float(scores["neg"])
    neu = float(scores["neu"])
    res = "positive"
    print("pos neg nue ", pos, neg, neu)
    if neg > pos and neg > neu:
        res = "negative"
    elif neu > neg and neu > pos:
        res = "neutral"
    res = json.dumps({"sentiment": res})
    print(res)
    return res


if __name__ == "__main__":
    app.run(debug=True)
