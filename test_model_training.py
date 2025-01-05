import unittest
from src.model_training import train_model
import os

class TestModelTraining(unittest.TestCase):
    def test_train_model(self):
        # Assuming you have a small sample CSV file for testing
        data_path = "tests/sample_data.csv"
        features = ["feature1", "feature2"]
        target = "target_column"
        
        # Create a small dataset if it doesn't exist
        if not os.path.exists(data_path):
            import pandas as pd
            data = pd.DataFrame({
                "feature1": [1, 2, 3, 4, 5],
                "feature2": [5, 4, 3, 2, 1],
                "target_column": [1, 0, 1, 0, 1]
            })
            data.to_csv(data_path, index=False)
        
        results = train_model(data_path, features, target)
        self.assertIsInstance(results["model"], object)  # Check if model is returned
        self.assertGreater(results["mse"], 0)  # Ensure MSE is computed
        self.assertIn("feature1", results["feature_importance"])  # Check feature importance
        
if __name__ == "__main__":
    unittest.main()
