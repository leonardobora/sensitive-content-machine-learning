import pandas as pd
import numpy as np # For np.nan

# 1. Load Data
try:
    df = pd.read_csv('data/raw/all_songs_data_processed.csv')
except FileNotFoundError:
    print("Error: 'data/raw/all_songs_data_processed.csv' not found. Please ensure it was created in previous steps.")
    exit()

# 2. Add New Columns
df['Manual_Score'] = np.nan # Initialize with NaN (float64 by default)
df['Labeling_Notes'] = pd.Series(dtype='object') # Initialize with NaN (object dtype for strings)

# 3. Populate Initial Rows (first 3 rows, i.e., index 0, 1, 2)
scores = [0.1, 0.8, 0.5]
notes = ["Mildly suggestive", "Explicit content", "References to violence"]

# Ensure we don't go out of bounds if the DataFrame has fewer than 3 rows
num_rows_to_label = min(3, len(df))

for i in range(num_rows_to_label):
    df.loc[i, 'Manual_Score'] = scores[i]
    df.loc[i, 'Labeling_Notes'] = notes[i]

# 4. Save the modified DataFrame (directory already created by bash)
output_path = 'data/labeled/manually_labeled_songs.csv'
try:
    df.to_csv(output_path, index=False)
    print(f"DataFrame saved to {output_path}")
except Exception as e:
    print(f"Error saving DataFrame: {e}")
    exit()

# 8. Print the head of the modified DataFrame
print("\nModified DataFrame head:")
print(df.head())
