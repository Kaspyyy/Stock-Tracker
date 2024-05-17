from django.shortcuts import render, get_object_or_404
from .utils import fetch_stock_data, fetch_news_data, analyze_sentiment, predict_sentiment, plot_sentiment_vs_price, plot_historical_data, cache_news_data, fetch_stock_data_longterm
from django.http import JsonResponse
from .models import Stock



# Create your views here.

def Home(request):

    stocks = Stock.objects.all()

    return render(request, 'home.html', {'stocks': stocks})



def Analytics(request, symbol):

    stock = get_object_or_404(Stock, symbol=symbol)

    context = {'stock': stock}

    return render(request, 'analytics.html', context)


def get_stock_plots(request, symbol):

    news_api_key = 'b9a3b4dbca9a4b3183ab0579ce9720f9'
    from_date = '2023-12-16'
    to_date = '2023-11-20'

    # Fetch stock data
    stock_data = fetch_stock_data(symbol)
    stock_data_longterm = fetch_stock_data_longterm(symbol)

    # Fetch news data
    news_df = cache_news_data(news_api_key, symbol, from_date, to_date)

    if news_df.empty:
        # Log that the DataFrame is empty
        print(f"No news data found for {symbol} from {from_date} to {to_date}")
    else:
        # Log the successful retrieval and the size of the DataFrame
        print(f"Retrieved news data for {symbol}: {len(news_df)} records found")

    latest_news = news_df.head(20)[['title', 'url']].to_dict(orient='records')
    # latest_news_links = news_df.head(10)[['url']].to_dict(orient='records')

    # print(latest_news_links)

    # Analyze sentiment
    classifier, vectorizer = analyze_sentiment(news_df)

    # Predict sentiment and plot
    sent_and_stock = predict_sentiment(stock_data, news_df, symbol, classifier, vectorizer)
    plot_sentiment_vs_price(sent_and_stock, symbol)

    # Plot historical data
    plot_historical_data(stock_data_longterm, symbol)

    sentiment_plot_url = f"/media/predicted/{symbol}_sentiment_plot.png"
    historical_plot_url = f"/media/historical/{symbol}_historical_plot.png"

    return JsonResponse({
        'sentiment_plot_url': sentiment_plot_url,
        'historical_plot_url': historical_plot_url,
        'latest_news': latest_news,
        # 'latest_news_links': latest_news_links
    })

def get_latest_news(request, symbol):
    # Assuming you have a function to fetch the latest news
    news_api_key = 'b9a3b4dbca9a4b3183ab0579ce9720f9'
    from_date = '2023-12-16'
    to_date = '2023-11-20'

    news_df = cache_news_data(news_api_key, symbol, from_date, to_date)

    # Get the latest 10 news headlines
    latest_news = news_df.head(10)[['title']].to_dict(orient='records')

    return JsonResponse({'latest_news': latest_news})
