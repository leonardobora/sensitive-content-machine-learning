import kagglehub
import pandas as pd
import os
from pathlib import Path

class KaggleDataLoader:
    """Handler for loading and managing Kaggle datasets."""
    
    def __init__(self, dataset_name="brianblakely/top-100-songs-and-lyrics-from-1959-to-2019"):
        self.dataset_name = dataset_name
        self.data_dir = Path(__file__).parent.parent.parent / "data" / "raw"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def load_dataset(self, file_path=""):
        """Load dataset from Kaggle using kagglehub."""
        try:
            print("Loading dataset: {}".format(self.dataset_name))
            
            # Download dataset files to local directory
            path = kagglehub.dataset_download(self.dataset_name)
            print("Dataset downloaded to: {}".format(path))
            
            # Find CSV files in the downloaded directory
            csv_files = list(Path(path).glob("*.csv"))
            if not csv_files:
                raise ValueError("No CSV files found in downloaded dataset")
            
            # Load the first CSV file found
            csv_file = csv_files[0]
            print("Loading CSV file: {}".format(csv_file))
            df = pd.read_csv(csv_file)
            
            print("Dataset loaded successfully. Shape: {}".format(df.shape))
            print("Columns: {}".format(list(df.columns)))
            
            # Save to local data directory
            local_path = self.data_dir / "songs_lyrics_dataset.csv"
            df.to_csv(local_path, index=False)
            print("Dataset saved to: {}".format(local_path))
            
            return df
            
        except Exception as e:
            print("Error loading dataset: {}".format(e))
            raise
    
    def get_dataset_info(self, df):
        """Display basic information about the dataset."""
        print("\n=== Dataset Information ===")
        print("Shape: {}".format(df.shape))
        print("Columns: {}".format(list(df.columns)))
        print("Data types:\n{}".format(df.dtypes))
        print("\nMissing values:\n{}".format(df.isnull().sum()))
        print("\nFirst 5 records:\n{}".format(df.head()))
        
        return {
            'shape': df.shape,
            'columns': list(df.columns),
            'missing_values': df.isnull().sum().to_dict(),
            'dtypes': df.dtypes.to_dict()
        }

if __name__ == "__main__":
    loader = KaggleDataLoader()
    df = loader.load_dataset()
    info = loader.get_dataset_info(df)