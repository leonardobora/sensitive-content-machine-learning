import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import os
import string
import nltk

# --- NLTK Resource Download & Cleaning Function (from previous subtasks) ---
os.makedirs('data/processed', exist_ok=True) # Ensure dir exists
try:
    nltk.data.find('tokenizers/punkt')
except LookupError: nltk.download('punkt', quiet=True)
try:
    nltk.data.find('corpora/stopwords')
except LookupError: nltk.download('stopwords', quiet=True)
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError: nltk.download('punkt_tab', quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def clean_lyrics_text(text_series):
    texts = text_series.fillna('').astype(str)
    texts = texts.str.lower()
    texts = texts.apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)))
    stop_words_set = set(stopwords.words('english'))
    def remove_stopwords_func(text):
        if not text.strip(): return ""
        tokens = word_tokenize(text)
        filtered_tokens = [word for word in tokens if word not in stop_words_set]
        return " ".join(filtered_tokens)
    texts = texts.apply(remove_stopwords_func)
    return texts

# --- Main script ---
# 2. Load Model
model_path = 'data/processed/lstm_model.keras'
try:
    model = load_model(model_path)
    print(f"Model loaded from {model_path}")
    # Get vocabulary size from the loaded model's embedding layer
    try:
        model_vocab_size = model.get_layer(index=0).input_dim
        print(f"Loaded model's vocabulary size (input_dim): {model_vocab_size}")
    except Exception as e:
        print(f"Could not determine model's vocabulary size from loaded model: {e}")
        model_vocab_size = 5000 # Fallback, though risky

except Exception as e:
    print(f"Error loading model: {e}. Exiting.")
    exit()

# 3. Load Data that was used for Training to Re-Fit Tokenizer
# This data must be identical to the  used in Subtask 4.
tokenizer_training_data_path = 'data/labeled/manually_labeled_songs.csv'
try:
    df_for_tokenizer = pd.read_csv(tokenizer_training_data_path)
    print(f"Loaded data for tokenizer fitting from {tokenizer_training_data_path}")

    # Ensure 'Cleaned_Lyrics' exists, or generate it (as done in Subtask 4)
    if 'Cleaned_Lyrics' not in df_for_tokenizer.columns or df_for_tokenizer['Cleaned_Lyrics'].isnull().all():
        print("'Cleaned_Lyrics' not found or all NaN in tokenizer data. Generating from 'lyrics'.")
        if 'lyrics' in df_for_tokenizer.columns:
            df_for_tokenizer['Cleaned_Lyrics'] = clean_lyrics_text(df_for_tokenizer['lyrics'])
        else:
            print("Critical: 'lyrics' column also missing in tokenizer data. Cannot form tokenizer basis. Exiting.")
            exit()

    # Filter and augment to match Subtask 4's
    labeled_df_for_tokenizer = df_for_tokenizer[df_for_tokenizer['Manual_Score'].notna()].copy()
    if len(labeled_df_for_tokenizer) < 3:
        print(f"Found only {len(labeled_df_for_tokenizer)} labeled samples in {tokenizer_training_data_path} for tokenizer. Augmenting.")
        if not labeled_df_for_tokenizer.empty:
            original_count = len(labeled_df_for_tokenizer)
            while len(labeled_df_for_tokenizer) < 3:
                new_rows = labeled_df_for_tokenizer.iloc[:original_count].copy()
                new_rows['Cleaned_Lyrics'] = new_rows['Cleaned_Lyrics'].astype(str) + " copy"
                new_rows['Manual_Score'] = np.clip(new_rows['Manual_Score'] * 0.9, 0.0, 1.0) # Score modification doesn't affect tokenizer
                labeled_df_for_tokenizer = pd.concat([labeled_df_for_tokenizer, new_rows], ignore_index=True)
                if len(labeled_df_for_tokenizer) >= 3: break
        else: # No labeled data at all
            print("No labeled data in {tokenizer_training_data_path} to fit tokenizer. Using minimal dummy.")
            # This case means the tokenizer will be very different from training.
            labeled_df_for_tokenizer = pd.DataFrame({
                'Cleaned_Lyrics': ["dummy lyric one", "dummy lyric two clean", "dummy lyric three four clean"],
                'Manual_Score': [0.1,0.2,0.3] # Scores not used for tokenizer fitting
            })

    tokenizer_texts = labeled_df_for_tokenizer['Cleaned_Lyrics'].astype(str).tolist()

except FileNotFoundError:
    print(f"Error: Tokenizer data file {tokenizer_training_data_path} not found. Exiting as tokenizer cannot be reliably refit.")
    exit()

# Initialize Tokenizer: Use model_vocab_size for num_words if available and smaller
# The key is that words mapped to indices >= model_vocab_size from the new fit must be treated as OOV by model
# The Tokenizer's num_words should be based on its own fit, but we must respect model_vocab_size for sequences.
tokenizer = Tokenizer(oov_token="<unk>") # num_words will be set by its own fit
tokenizer.fit_on_texts(tokenizer_texts)
fitted_tokenizer_vocab_size = len(tokenizer.word_index) + 1
print(f"Tokenizer fitted on reconstructed training texts. Own vocab size: {fitted_tokenizer_vocab_size}")


# 4. Load Full Dataset
full_data_path = 'data/raw/all_songs_data_processed.csv'
try:
    df_full = pd.read_csv(full_data_path)
    print(f"Full dataset loaded from {full_data_path}")
except FileNotFoundError:
    print(f"Error: Full dataset {full_data_path} not found. Creating a dummy for demonstration.")
    df_full = pd.DataFrame({
        'id': range(5), 'artist_name': list('ABCDE'), 'track_name': [f'Track {i}' for i in range(5)],
        'release_date': ['2000-01-01', '2001-05-10', '2000-10-20', '2002-03-15', '2001-12-01'],
        'lyrics': ["Sample lyric one!", "Another THE great song.", "Third song, very good.", "Fourth with punctuation!!", "Fifth and final example lyric."]
    })

# 5. Prepare Full Dataset Lyrics
if 'Cleaned_Lyrics' not in df_full.columns or df_full['Cleaned_Lyrics'].isnull().all():
    print("Generating 'Cleaned_Lyrics' for the full dataset from 'lyrics' column.")
    if 'lyrics' in df_full.columns:
        df_full['Cleaned_Lyrics'] = clean_lyrics_text(df_full['lyrics'])
    else:
        print("Error: 'lyrics' column missing in full dataset. Cannot generate 'Cleaned_Lyrics'. Exiting.")
        exit()

lyrics_full_processed = df_full['Cleaned_Lyrics'].astype(str).tolist()
sequences_full = tokenizer.texts_to_sequences(lyrics_full_processed)

# Critical step: Cap token indices at model_vocab_size - 1. OOV token will handle others.
# The tokenizer might have a larger vocab from its own fit if the texts differed.
# Any token index >= model_vocab_size from tokenizer.texts_to_sequences must be treated as OOV by the model.
# The oov_token in tokenizer is usually mapped to index 1.
# If a word's index from tokenizer.word_index is >= model_vocab_size, it should effectively be an OOV word for the model.
# Keras Tokenizer's texts_to_sequences with oov_token handles words not in its *own* fit.
# The problem is when a word *is* in its own fit, but its index is too high for the *model's* embedding layer.
# We need to manually cap indices or ensure tokenizer's num_words is set to model_vocab_size *before* texts_to_sequences.

# Let's try re-creating tokenizer with num_words = model_vocab_size from the start
# This will ensure that texts_to_sequences itself maps words outside this top N to oov_token_index
print(f"Re-initializing tokenizer with num_words = {model_vocab_size} (from loaded model) for sequence generation.")
tokenizer_for_prediction = Tokenizer(num_words=model_vocab_size, oov_token="<unk>")
tokenizer_for_prediction.fit_on_texts(tokenizer_texts) # Fit on the same reconstructed training texts
sequences_full = tokenizer_for_prediction.texts_to_sequences(lyrics_full_processed)


maxlen = 100 # Same maxlen as used in training
padded_sequences_full = pad_sequences(sequences_full, maxlen=maxlen, padding='post', truncating='post')

# 6. Make Predictions
print(f"Making predictions with input shape: {padded_sequences_full.shape}")
predictions = model.predict(padded_sequences_full)

# 7. Add Predictions to DataFrame
df_full['Predicted_Score'] = predictions.flatten()

# 8. Simulate Analysis
print("\n--- Analysis ---")
song_identifier_col = 'track_name' if 'track_name' in df_full.columns else 'id'
# ... (rest of analysis and saving logic is the same as before)
print("\nTop 5 songs by Predicted_Score:")
top_5_songs = df_full.sort_values(by='Predicted_Score', ascending=False).head(5)
if song_identifier_col in top_5_songs.columns:
    print(top_5_songs[[song_identifier_col, 'Predicted_Score']])
else:
    temp_df = top_5_songs.copy()
    temp_df[song_identifier_col] = temp_df.index
    print(temp_df[[song_identifier_col, 'Predicted_Score']])

if 'release_date' in df_full.columns:
    df_full['Year'] = pd.to_datetime(df_full['release_date'], errors='coerce').dt.year
    if df_full['Year'].notna().any():
        avg_score_per_year = df_full.groupby('Year')['Predicted_Score'].mean().sort_values(ascending=False)
        print("\nAverage Predicted_Score per Year:")
        print(avg_score_per_year)
    else:
        print("\n'Year' column extracted, but all values are NaN. Skipping yearly analysis.")
else:
    print("\n'release_date' column not found. Skipping yearly analysis.")

# 9. Save Results
output_csv_path = 'data/processed/songs_with_predictions.csv'
try:
    df_full.to_csv(output_csv_path, index=False)
    print(f"\nDataFrame with predictions saved to {output_csv_path}")
except Exception as e:
    print(f"Error saving DataFrame to CSV: {e}")

# 10. Print head of the saved DataFrame
print("\nHead of saved DataFrame (songs_with_predictions.csv):")
print(df_full.head())
