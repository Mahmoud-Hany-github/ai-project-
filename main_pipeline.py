from src.api_handler import fetch_data_from_api
from src.preprocess_graph import preprocess_graph, validate_graph, parse_graph_file
from src.qlib_integration import prepare_qlib_data
from src.qlib_converter import convert_to_qlib_format
from src.main_pipeline import pipeline
from src.data_processing import fetch_and_process_api_data
from src.qlib_converter import convert_to_qlib_format
from src.qlib_integration import prepare_qlib_data
from src.preprocess_graph import parse_graph_file, validate_graph, preprocess_graph

# Step: Prepare Qlib data
def main():
    raw_data_dir = "data/raw/"
    processed_data_dir = "data/processed/qlib_data/"

    print("Fetching and processing API data...")
    fetch_and_process_api_data(raw_data_dir)
    print("API data fetched and saved.")

    print("Converting data to Qlib format...")
    convert_to_qlib_format(raw_data_dir, processed_data_dir)
    print("Data converted to Qlib-compatible format.")

    print("Initializing Qlib integration...")
    prepare_qlib_data(processed_data_dir)
    print("Qlib data preparation completed.")

if __name__ == "__main__":
    main()

import os

# Step: Fetch data from APIs and save to raw data directory
def fetch_and_save_api_data(raw_data_dir):
    # Define API targets
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

    print("Fetching data from APIs...")
    results, errors = {}, []

    # Fetch data from each API
    for api_name, params in targets.items():
        data = fetch_data_from_api(api_name, **params)
        if data:
            results[api_name] = data
        else:
            errors.append(api_name)
    
    # Save fetched data to raw data directory
    os.makedirs(raw_data_dir, exist_ok=True)
    output_path = os.path.join(raw_data_dir, "api_results.csv")
    convert_to_qlib_format(results, output_path)  # Save results in Qlib format-compatible CSV
    print(f"API data saved to {output_path}. Errors: {errors}")

# Step: Prepare Qlib data
def prepare_data_for_qlib(raw_data_dir, processed_data_dir):
    print("Preparing Qlib-compatible data...")
    prepare_qlib_data(raw_data_dir, processed_data_dir)
    print("Data preparation for Qlib completed.")

# Step: Graph processing
def process_graph(graph_file):
    print("Processing graph...")
    nodes, edges = parse_graph_file(graph_file)
    validate_graph(nodes, edges)
    processed_nodes, processed_edges = preprocess_graph(nodes, edges)
    print("Graph processing completed.")
    return processed_nodes, processed_edges

# Main function
def main():
    raw_data_dir = "data/raw/"
    processed_data_dir = "data/processed/qlib_data/"
    graph_file = "data/graph.json"

    # Step 1: Fetch data from APIs
    fetch_and_save_api_data(raw_data_dir)

    # Step 2: Prepare Qlib data
    prepare_data_for_qlib(raw_data_dir, processed_data_dir)

    # Step 3: Graph processing
    processed_nodes, processed_edges = process_graph(graph_file)

    # Step 4: Execute the main pipeline (example functionality, modify as needed)
    print("Running the main pipeline...")
    pipeline(processed_nodes, processed_edges, processed_data_dir)
    print("Pipeline execution completed.")

if __name__ == "__main__":
    main()
