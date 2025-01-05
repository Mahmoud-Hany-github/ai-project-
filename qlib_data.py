from qlib.data.dataset import DatasetH
from qlib.data.dataset.handler import DataHandlerLP

# Configuration for Qlib dataset
handler_config = {
    "start_time": "2008-01-01",
    "end_time": "2023-12-31",
    "fit_start_time": "2008-01-01",
    "fit_end_time": "2023-12-31",
    "instruments": "csi300",  # Replace with your instrument set if different
}

def load_and_explore_data():
    print("Loading Qlib dataset...")
    dataset = DatasetH(handler_class=DataHandlerLP, handler_kwargs=handler_config)
    print("Dataset loaded successfully!")

    # Print basic dataset information
    print("\nDataset Summary:")
    print(dataset)

if __name__ == "__main__":
    load_and_explore_data()
