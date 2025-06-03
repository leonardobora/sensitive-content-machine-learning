import pandas as pd

# Load the dataframe
df = pd.read_csv('data/raw/all_songs_data_processed.csv')

# Print the first 5 rows
print("DataFrame Head:")
print(df.head())

# Print DataFrame info
print("\nDataFrame Info:")
df.info()
