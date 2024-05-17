# stock_sentiment/utils.py
import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from newsapi import NewsApiClient
import plotly.graph_objs as go
import plotly.offline as pyo
import shelve
import datetime
import os


def fetch_stock_data(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    return stock.history(period="7d")

def fetch_stock_data_longterm(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    return stock.history(period="3mo")


def plot_historical_data(stock_data, symbol):
    plt.figure(figsize=(10, 5))
    stock_data['Open'].plot(label='Open Price')
    plt.title(f"{symbol} Historical Stock Data")
    plt.xlabel("Date")
    plt.ylabel("Open Price")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"media/historical/{symbol}_historical_plot.png")  # Save the plot to media folder


# def plot_historical_data(stock_data, symbol):
#     trace = go.Scatter(x=stock_data.index, y=stock_data['Open'], mode='lines', name='Open Price')
#     layout = go.Layout(title=f"{symbol} Historical Stock Data", xaxis=dict(title='Date'), yaxis=dict(title='Open Price'))
#     fig = go.Figure(data=[trace], layout=layout)

#     # Save the figure as an HTML file
#     file_path = f"media/historical/{symbol}_historical_plot.html"
#     pyo.plot(fig, filename=file_path, auto_open=False)




def fetch_news_data(api_key, symbol, from_date, to_date):
    query = f"{symbol} stock"
    newsapi = NewsApiClient(api_key=api_key)
    source_data = newsapi.get_everything(q=query, from_param=from_date, to=to_date, language='en', page_size=100)
    articles = source_data['articles']
    return pd.DataFrame(articles)

def cache_news_data(news_api_key, stock_symbol, from_date, to_date, cache_duration_hours=24):
    cache_file = 'news_cache.db'  # File to store cached data
    cache_key = f"{stock_symbol}_{from_date}_{to_date}"  # Unique key for each query

    # Open the cache file
    with shelve.open(cache_file) as cache:
        # Check if data is already cached and is still valid
        if cache_key in cache:
            cached_data, timestamp = cache[cache_key]
            if (datetime.datetime.now() - timestamp) < datetime.timedelta(hours=cache_duration_hours):
                return cached_data  # Return cached data if it's still valid

        # If data is not cached or cache is expired, fetch new data
        news_data = fetch_news_data(news_api_key, stock_symbol, from_date, to_date)

        # Cache the new data with a timestamp
        cache[cache_key] = (news_data, datetime.datetime.now())

def analyze_sentiment(news_df):
    news_df["score"] = news_df["content"].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X = vectorizer.fit_transform(news_df["content"])
    y = (news_df["score"] > 0).astype(int)
    randomclassifier_sent = RandomForestClassifier(n_estimators=200, criterion='entropy', random_state=42)
    randomclassifier_sent.fit(X, y)
    return randomclassifier_sent, vectorizer

def predict_sentiment(stock_data, news_df, symbol, classifier, vectorizer):
    # Check if 'symbol' column exists in news_df
    if 'symbol' in news_df.columns:
        filtered_news_df = news_df[news_df['symbol'] == symbol]
    else:
        # If no 'symbol' column, assume news_df is already specific to the symbol
        filtered_news_df = news_df

    # Ensure that the DataFrame is not empty
    if filtered_news_df.empty:
        # Handle the case where there is no relevant news data
        return pd.DataFrame()  # or other appropriate handling

    # Proceed with sentiment prediction
    live_news_features = vectorizer.transform(filtered_news_df["content"])
    filtered_news_df["PredictedSentiment"] = classifier.predict(live_news_features)

    if not pd.api.types.is_datetime64_any_dtype(filtered_news_df['publishedAt']):
        filtered_news_df['publishedAt'] = pd.to_datetime(filtered_news_df['publishedAt'])

    filtered_news_df['Date'] = filtered_news_df['publishedAt'].dt.date

    sent_daily = filtered_news_df.groupby("Date")[["score", "PredictedSentiment"]].mean()

    clx_df = stock_data.copy()
    clx_df["Date"] = clx_df.index.date
    clx_df = clx_df.set_index("Date")

    sent_and_stock = sent_daily.merge(clx_df, left_index=True, right_index=True)

    return sent_and_stock


# def predict_sentiment(stock_data, news_df, symbol, classifier, vectorizer):
#     live_news_features = vectorizer.transform(news_df[news_df['symbol'] == symbol]["content"])
#     news_df.loc[news_df['symbol'] == symbol, "PredictedSentiment"] = classifier.predict(live_news_features)
#     news_df.loc[news_df['symbol'] == symbol, 'Date'] = news_df[news_df['symbol'] == symbol]['publishedAt'].dt.date

#     sent_daily = news_df[news_df['symbol'] == symbol].groupby("Date")[["score", "PredictedSentiment"]].mean()

#     clx_df = stock_data.copy()
#     clx_df["Date"] = clx_df.index.date
#     clx_df = clx_df.set_index("Date")

#     sent_and_stock = sent_daily.merge(clx_df, left_index=True, right_index=True)

#     return sent_and_stock

def plot_sentiment_vs_price(sent_and_stock, symbol):
    sent_and_stock_reset = sent_and_stock.reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    color_sentiment_bar = 'tab:green'
    ax.set_xlabel('Date')
    ax.set_ylabel('Predicted Sentiment', color=color_sentiment_bar)
    sns.barplot(x='Date', y='PredictedSentiment', data=sent_and_stock_reset, ax=ax, color=color_sentiment_bar, label='Sentiment')
    ax.tick_params(axis='y', labelcolor=color_sentiment_bar)
    ax.legend(loc='upper left')

    ax2 = ax.twinx()
    color_price_bar = 'tab:orange'
    ax2.set_ylabel('Closing Price', color=color_price_bar)
    sns.barplot(x='Date', y='Close', data=sent_and_stock_reset, ax=ax2, color=color_price_bar, alpha=0.7, label='Closing Price')
    ax2.tick_params(axis='y', labelcolor=color_price_bar)
    ax2.legend(loc='upper right')

    fig.tight_layout(pad=3.0)
    plt.title(f"{symbol} Predicted Sentiment and Closing Price Analysis")
    plt.savefig(f"media/predicted/{symbol}_sentiment_plot.png")  # Save the plot to media folder



# def plot_sentiment_vs_price(sent_and_stock, symbol):
#     sent_and_stock_reset = sent_and_stock.reset_index()

#     # Create traces
#     trace1 = go.Bar(x=sent_and_stock_reset['Date'], y=sent_and_stock_reset['PredictedSentiment'], name='Predicted Sentiment', marker_color='green')
#     trace2 = go.Scatter(x=sent_and_stock_reset['Date'], y=sent_and_stock_reset['Close'], mode='lines', name='Closing Price', yaxis='y2')

#     layout = go.Layout(
#         title=f"{symbol} Predicted Sentiment and Closing Price Analysis",
#         xaxis=dict(title='Date'),
#         yaxis=dict(title='Predicted Sentiment'),
#         yaxis2=dict(title='Closing Price', overlaying='y', side='right'),
#         legend=dict(x=0.1, y=1.1, orientation="h")
#     )

#     fig = go.Figure(data=[trace1, trace2], layout=layout)

#     # Save the figure as an HTML file
#     file_path = f"media/predicted/{symbol}_sentiment_vs_price.html"
#     pyo.plot(fig, filename=file_path, auto_open=False)






    # https://iexcloud.io/console/manage-plan

