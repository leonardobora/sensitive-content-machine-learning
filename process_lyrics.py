import pandas as pd
import string
import nltk

# Download nltk resources if not already present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading NLTK resource: punkt")
    nltk.download('punkt', quiet=True)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Downloading NLTK resource: stopwords")
    nltk.download('stopwords', quiet=True)
try:
    nltk.data.find('tokenizers/punkt_tab') # Added this check
except LookupError:
    print("Downloading NLTK resource: punkt_tab")
    nltk.download('punkt_tab', quiet=True) # Added punkt_tab download

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Load the dataframe
df = pd.read_csv('data/raw/all_songs_data_processed.csv')

print("Original DataFrame head (all rows for this dummy data):")
print(df)

# --- 1. Initial check for missing values in 'lyrics' ---
print("\nMissing values in 'lyrics' before cleaning (isnull()):")
print(df['lyrics'].isnull().sum())
print("Empty strings in 'lyrics' before cleaning (value == ''):")
print(df[df['lyrics'] == ''].shape[0])


# --- 2. Clean the 'Lyrics' column ---
# Create a working series from 'lyrics', fill NaN with empty string for processing
# This ensures that rows with NaN lyrics become empty strings after cleaning, not errors.
lyrics_for_cleaning = df['lyrics'].fillna('')

# a. Convert to lowercase
cleaned_lyrics_series = lyrics_for_cleaning.str.lower()

# b. Remove punctuation
cleaned_lyrics_series = cleaned_lyrics_series.apply(lambda x: str(x).translate(str.maketrans('', '', string.punctuation)))

# c. Remove stopwords
stop_words = set(stopwords.words('english'))

def remove_stopwords(text):
    if not text.strip(): # Handle strings that are empty or become empty after punctuation removal
        return ""
    tokens = word_tokenize(text) # word_tokenize expects a string
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return " ".join(filtered_tokens)

cleaned_lyrics_series = cleaned_lyrics_series.apply(remove_stopwords)

# --- 3. Create 'Cleaned_Lyrics' column ---
df['Cleaned_Lyrics'] = cleaned_lyrics_series

# --- 4. Check for missing/empty values in 'Cleaned_Lyrics' ---
print("\nMissing values in 'Cleaned_Lyrics' after cleaning (isnull()):")
# isnull() will be 0 because NaNs were converted to empty strings before processing.
print(df['Cleaned_Lyrics'].isnull().sum())
print("Empty strings in 'Cleaned_Lyrics' after cleaning (value == ''):")
# This counts rows where lyrics became empty after all cleaning steps.
# (e.g. original was NaN, or original was "" or original was just stopwords/punctuation)
print(df[df['Cleaned_Lyrics'] == ''].shape[0])


# --- 5. Print the 'Lyrics' and 'Cleaned_Lyrics' ---
print("\nLyrics vs Cleaned_Lyrics (all rows for this dummy data):")
print(df[['lyrics', 'Cleaned_Lyrics']])
