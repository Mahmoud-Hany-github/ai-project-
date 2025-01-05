import urllib.request
import urllib.parse
import json
import heapq
import time
from datetime import datetime
import csv
import json

# Example API results (replace this with your actual API results)
api_results = {
    "Alpha Vantage": {"ticker": "AAPL", "data": {"price": 150}},
    "Binance": {"crypto_symbol": "BTCUSDT", "data": {"price": 50000}},
    "News API": {"keyword": "stock market", "articles": ["Article 1", "Article 2"]},
    "Errors": ["Polygon.io", "Quandl(Fred)"]
}

# Define CSV file path
output_csv_file = "api_results.csv"

# Process and save to CSV
def save_to_csv(results, file_path):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(["API Name", "Parameter", "Result"])
        
        # Write API results
        for api_name, data in results.items():
            if api_name != "Errors":
                for key, value in data.items():
                    writer.writerow([api_name, key, value])
        
        # Write errors, if any
        if "Errors" in results and results["Errors"]:
            writer.writerow([])
            writer.writerow(["Errors"])
            for error in results["Errors"]:
                writer.writerow([error])

# Save results to CSV
save_to_csv(api_results, output_csv_file)

print(f"Results saved to {output_csv_file}")

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

# Fetch data from an API
def fetch_data_from_api(api_name, **kwargs):
    if api_name not in api_config:
        print(f"Error: API '{api_name}' is not configured.")
        return None

    config = api_config[api_name]
    endpoint = config["endpoint"]

    # Replace placeholders with parameters
    for param in config["params"]:
        if param not in kwargs:
            print(f"Error: Missing required parameter '{param}' for API '{api_name}'.")
            return None
        value = urllib.parse.quote(kwargs[param])
        endpoint = endpoint.replace(f"{{{param}}}", value)

    # Add API key if required
    if "api_key" in endpoint and config["api_key"]:
        endpoint = endpoint.replace("{api_key}", config["api_key"])

    try:
        with urllib.request.urlopen(endpoint) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching data from {api_name}: {e}")
        return None

# Extract latest data from API response
def extract_latest_data(api_name, data):
    if api_name == "Alpha Vantage":
        daily_data = data.get("Time Series (Daily)", {})
        latest_date = max(daily_data.keys()) if daily_data else None
        return {latest_date: daily_data.get(latest_date)} if latest_date else "No data available."

    elif api_name == "Binance":
        return {"price": data.get("price", "N/A")}

    elif api_name == "News API":
        articles = data.get("articles", [])
        return articles[:5]  # Return the latest 5 articles

    elif api_name == "Quandl(Fred)":
        dataset = data.get("dataset", {})
        latest_date = dataset.get("end_date", "N/A")
        return {"end_date": latest_date, "data": dataset.get("data", [])[:5]}  # Latest 5 records

    elif api_name == "Polygon.io (Real-time stock quote)":
        return {"price": data.get("last", {}).get("price", "N/A")}

    elif api_name == "Quandl(Wiki)":
        dataset = data.get("dataset", {})
        latest_date = dataset.get("end_date", "N/A")
        return {"end_date": latest_date, "data": dataset.get("data", [])[:5]}  # Latest 5 records

    elif api_name == "Twitter API":
        tweets = data.get("data", [])
        return tweets[:5]  # Return the latest 5 tweets

    elif api_name == "Reddit API":
        posts = data.get("data", {}).get("children", [])
        return [post["data"] for post in posts[:5]]  # Latest 5 posts

    elif api_name == "Yahoo Finance API":
        summary = data.get("summaryProfile", {})
        return summary  # Return the full summary

    return "No relevant data available."

# A* algorithm to fetch data
def a_star_api_execution(targets):
    open_set = []
    results = {}
    errors = []

    # Initialize the priority queue with all APIs
    for api_name in targets:
        heapq.heappush(open_set, (heuristic(api_name), api_name, targets[api_name]))

    while open_set:
        _, api_name, params = heapq.heappop(open_set)
        print(f"\nFetching data from {api_name}...")

        data = fetch_data_from_api(api_name, **params)
        if data:
            results[api_name] = extract_latest_data(api_name, data)
            print(f"{api_name} fetched successfully.")
        else:
            print(f"{api_name} failed to fetch data.")
            errors.append(api_name)

    return results, errors

# Main function to demonstrate the implementation
import time
import json
from datetime import datetime

def main():
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

    start_time = time.time()
    print("Starting API fetch using A* prioritization...")
    
    # Fetch results and errors
    results, errors = a_star_api_execution(targets)
    end_time = time.time()

    # Add unique timestamps for each API's data
    results_with_timestamps = {}
    for api_name, result in results.items():
        results_with_timestamps[api_name] = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": result
        }

    # Combine all results into a single JSON object
    combined_results = {
        "results": results_with_timestamps,
        "errors": errors,
        "fetch_time": f"{end_time - start_time:.2f} seconds",
    }

    # Save combined results to a file or display them
    print("\n============================")
    print("Combined API Fetch Results:")
    print("============================")
    print(json.dumps(combined_results, indent=4))

    # Save to a JSON file
    with open("api_results_with_timestamps.json", "w") as file:
        json.dump(combined_results, file, indent=4)

if __name__ == "__main__":
    main()
