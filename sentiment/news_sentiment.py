import feedparser
from textblob import TextBlob
from alerts.telegram_alert import send_telegram_alert

def analyze_news_sentiment():
    symbol = input("Enter NSE stock symbol: ").upper()

    # Remove .NS if user enters it
    if symbol.endswith(".NS"):
        symbol = symbol.replace(".NS", "")

    print(f"\nFetching latest news for {symbol}...")

    # Google News RSS feed
    rss_url = f"https://news.google.com/rss/search?q={symbol}+stock+India&hl=en-IN&gl=IN&ceid=IN:en"

    feed = feedparser.parse(rss_url)

    if not feed.entries:
        print("No recent news found.")
        return

    positive = 0
    negative = 0
    neutral = 0

    print("\n" + "=" * 90)
    print(f"                NEWS & SENTIMENT ANALYSIS - {symbol}")
    print("=" * 90)

    # Analyze top 10 news headlines
    for idx, entry in enumerate(feed.entries[:10], start=1):
        headline = entry.title

        # Sentiment analysis
        analysis = TextBlob(headline)
        polarity = analysis.sentiment.polarity

        if polarity > 0.1:
            sentiment = "Positive"
            positive += 1
        elif polarity < -0.1:
            sentiment = "Negative"
            negative += 1
        else:
            sentiment = "Neutral"
            neutral += 1

        print(f"\n{idx}. {headline}")
        print(f"   Sentiment: {sentiment} (Score: {polarity:.2f})")

    # Overall sentiment score
    total = positive + negative + neutral
    sentiment_score = ((positive - negative) / total) * 100

    print("\n" + "-" * 90)
    print("OVERALL SENTIMENT SUMMARY")
    print("-" * 90)
    print(f"Positive News: {positive}")
    print(f"Negative News: {negative}")
    print(f"Neutral News : {neutral}")
    print(f"Sentiment Score: {sentiment_score:.2f}")

    # Final recommendation
    if sentiment_score > 30:
        recommendation = "STRONG POSITIVE"
    elif sentiment_score > 10:
        recommendation = "POSITIVE"
    elif sentiment_score < -30:
        recommendation = "STRONG NEGATIVE"
    elif sentiment_score < -10:
        recommendation = "NEGATIVE"
    else:
        recommendation = "NEUTRAL"

    print(f"Overall Sentiment: {recommendation}")
    print("=" * 90)

    # Send Telegram alert for strong sentiment
    if recommendation in ["STRONG POSITIVE", "STRONG NEGATIVE"]:
        message = (
            f"📰 StockAI News Alert: {symbol}\n\n"
            f"Overall Sentiment: {recommendation}\n"
            f"Sentiment Score: {sentiment_score:.2f}\n\n"
            f"Positive: {positive} | Negative: {negative} | Neutral: {neutral}"
        )
        send_telegram_alert(message)
        print("Telegram sentiment alert sent!")