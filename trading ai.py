import urllib.request
import urllib.parse
import json
import heapq
import time
import schedule
import csv
import alpaca_trade_api as tradeapi
import qlib


# API configuration with provided keys and endpoints
api_config = {
    "Alpha Vantage": {
        "endpoint": "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}",
        "params": ["ticker"],
        "api_key": "0YNETGYCAKM666US",
    },
    "Binance": {
        "endpoint": "https://api.binance.com/api/v3/ticker/price?symbol={crypto_symbol}",
        "params": ["crypto_symbol"],
        "api_key": None,  # Binance does not require an API key
    },
    "News API": {
        "endpoint": "https://newsapi.org/v2/everything?q={keyword}&apiKey={api_key}",
        "params": ["keyword"],
        "api_key": "34eeb17f02804e75a32de8b1b5435d43",
    },
    "Quandl(Fred)": {
        "endpoint": "https://www.quandl.com/api/v3/datasets/FRED/{dataset_code}.json?api_key={api_key}",
        "params": ["dataset_code"],
        "api_key": "AdAcT-CtrM1e1uP8Ug3N",
    },
    "Polygon.io (Real-time stock quote)": {
        "endpoint": "https://api.polygon.io/v1/last/stocks/{ticker}?apiKey={api_key}",
        "params": ["ticker"],
        "api_key": "DxzT5yWFevexWdxVcRB_okJhlsaBpPEE",
    },
    "Quandl(Wiki)": {
        "endpoint": "https://www.quandl.com/api/v3/datasets/WIKI/{ticker}.json?api_key={api_key}",
        "params": ["ticker"],
        "api_key": "AdAcT-CtrM1e1uP8Ug3N",
    },
    "Twitter API": {
        "endpoint": "https://api.twitter.com/2/tweets/search/recent?query={keyword}&max_results=100",
        "params": ["keyword"],
        "api_key": None,  # Requires OAuth token
    },
    "Reddit API": {
        "endpoint": "https://www.reddit.com/r/{subreddit}/new.json",
        "params": ["subreddit"],
        "api_key": None,  # Does not require API key
    },
    "Yahoo Finance API": {
        "endpoint": "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary?symbol={ticker}",
        "params": ["ticker"],
        "api_key": None,  # Requires RapidAPI key
    },
}

# Function to fetch data from an API
def fetch_data_from_api(api_name, **kwargs):
    config = api_config[api_name]
    endpoint = config["endpoint"]
    for param in config["params"]:
        value = urllib.parse.quote(kwargs[param])
        endpoint = endpoint.replace(f"{{{param}}}", value)
    if "api_key" in endpoint:
        endpoint = endpoint.replace("{api_key}", config["api_key"])

    try:
        with urllib.request.urlopen(endpoint) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching data from {api_name}: {e}")
        return None

# Function to extract latest data from API response
def extract_latest_data(api_name, data):
    if api_name == "Alpha Vantage":
        time_series = data.get("Time Series (1min)", {})
        latest_time = max(time_series.keys()) if time_series else None
        return {latest_time: time_series.get(latest_time)} if latest_time else "No data available."
    return "No relevant data available."

# Function to save API results to CSV
def save_to_csv(results, file_path):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["API Name", "Parameter", "Result"])
        for api_name, data in results.items():
            if api_name != "Errors":
                for key, value in data.items():
                    writer.writerow([api_name, key, value])
        if "Errors" in results and results["Errors"]:
            writer.writerow([])
            writer.writerow(["Errors"])
            for error in results["Errors"]:
                writer.writerow([error])

# Function to fetch and save API data
def fetch_and_save_api_data():
    targets = {
        "Alpha Vantage": {"ticker": "AAPL"},
        "Binance": {"crypto_symbol": "BTCUSDT"},
        "News API": {"keyword": "stock market"},
        "Quandl(Fred)": {"dataset_code": "GDP"},
        "Polygon.io (Real-time stock quote)": {"ticker": "TSLA"},
        "Quandl(Wiki)": {"ticker": "MSFT"},
        "Twitter API": {"keyword": "AI"},
        "Reddit API": {"subreddit": "technology"},
        "Yahoo Finance API": {"ticker": "GOOG"},
    }
    api_results, api_errors = a_star_api_execution(targets)
    save_to_csv(api_results, "api_results.csv")


# Heuristic function to prioritize APIs
def heuristic(api_name):
    priorities = {
        "Alpha Vantage": 1,
        "Binance": 2,
        "News API": 3,
        "Quandl(Fred)": 2,
        "Polygon.io (Real-time stock quote)": 1,
        "Quandl(Wiki)": 2,
        "Twitter API": 3,
        "Reddit API": 3,
        "Yahoo Finance API": 2,
    }
    return priorities.get(api_name, 5)

# A* algorithm to fetch data
def a_star_api_execution(targets):
    open_set = []
    results = {}
    errors = []

    for api_name in targets:
        heapq.heappush(open_set, (heuristic(api_name), api_name, targets[api_name]))

    while open_set:
        _, api_name, params = heapq.heappop(open_set)
        data = fetch_data_from_api(api_name, **params)
        if data:
            results[api_name] = extract_latest_data(api_name, data)
        else:
            errors.append(api_name)
    return results, errors

# Initialize Qlib and Alpaca API
qlib.init(provider_uri='~/.qlib/qlib_data/cn_data', region=REG_CN)
ALPACA_API_KEY = 'YOUR_ALPACA_API_KEY'
ALPACA_SECRET_KEY = 'YOUR_ALPACA_SECRET_KEY'
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, APCA_API_BASE_URL, api_version='v2')

# Function to retrain model and fetch API data
def retrain_model_and_fetch_data():
    fetch_and_save_api_data()
    market = "csi300"
    qlib_data = D.features(D.instruments(market), ["$close", "$volume"])
    train_data, test_data = qlib_data.split(0.8)
    model = LGBModel()
    model.fit(train_data)
    return model, test_data

# Function to make predictions and trade
def trade(model, test_data):
    prediction = model.predict(test_data)
    last_price = test_data.iloc[-1]["$close"]
    buy_signal = prediction > last_price
    if buy_signal:
        api.submit_order(
            symbol='AAPL',
            qty=1,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
    print("Trade executed based on the prediction.")

# Schedule the retrain and trade functions every minute
schedule.every().minute.do(lambda: trade(*retrain_model_and_fetch_data()))

while True:
    schedule.run_pending()
    time.sleep(1)
