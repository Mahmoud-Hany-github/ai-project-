from src.preprocess_graph import parse_graph_file, validate_graph, preprocess_graph
from src.api_fetch import fetch_data
from src.convert_to_qlib import convert_to_qlib_format

def main_pipeline(graph_file, input_csv, output_dir):
    # Step 1: Fetch API data
    print("Fetching API data...")
    fetch_data()

    # Step 2: Preprocess graph data
    try:
        print("Preprocessing graph data...")
        nodes, edges = parse_graph_file(graph_file)
        validate_graph(nodes, edges)
        processed_nodes, processed_edges = preprocess_graph(nodes, edges)
        print("Graph preprocessing successful!")
    except ValueError as e:
        print(f"Graph validation failed: {e}")
        return

    # Step 3: Convert data to Qlib format
    try:
        print("Converting data to Qlib format...")
        convert_to_qlib_format(input_csv, output_dir)
        print("Data conversion successful!")
    except Exception as e:
        print(f"Data conversion failed: {e}")
        return

    print("Pipeline completed successfully!")

if __name__ == "__main__":
    graph_file = "data/valid_graph.json"
    input_csv = "data/api_results_with_timestamps.csv"
    output_dir = "results/processed/"
    main_pipeline(graph_file, input_csv, output_dir)
