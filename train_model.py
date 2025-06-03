import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
import os
import string # For punctuation removal
import nltk   # For stopwords

# Ensure data/processed directory exists
os.makedirs('data/processed', exist_ok=True)

# --- NLTK Resource Download (from Subtask 2 logic) ---
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
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    print("Downloading NLTK resource: punkt_tab")
    nltk.download('punkt_tab', quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# --- Lyric Cleaning Function (from Subtask 2 logic) ---
def clean_lyrics_text(text_series):
    # Fill NaN values with an empty string
    texts = text_series.fillna('').astype(str)
    # Convert to lowercase
    texts = texts.str.lower()
    # Remove punctuation
    texts = texts.apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)))
    # Remove stopwords
    stop_words_set = set(stopwords.words('english'))
    def remove_stopwords_func(text):
        if not text.strip(): return ""
        tokens = word_tokenize(text)
        filtered_tokens = [word for word in tokens if word not in stop_words_set]
        return " ".join(filtered_tokens)
    texts = texts.apply(remove_stopwords_func)
    return texts

# 2. Load Data
try:
    df = pd.read_csv('data/labeled/manually_labeled_songs.csv')
    print("Successfully loaded 'data/labeled/manually_labeled_songs.csv'")
    print("Columns in loaded DataFrame:", df.columns.tolist())
except FileNotFoundError:
    print("Error: 'data/labeled/manually_labeled_songs.csv' not found. Creating dummy df.")
    # This dummy df needs to accurately reflect all expected columns
    data = {
        'id': [1,2,3,4,5], 'artist_name': ['A','B','C','D','E'], 'track_name': ['T1','T2','T3','T4','T5'],
        'release_date': ['2000-01-01']*5, 'genre': ['Pop']*5, 'length': [200]*5, 'tempo': [120]*5,
        'danceability': [0.5]*5, 'energy': [0.7]*5, 'loudness': [-5.0]*5,
        'lyrics': ["First lyric example!", "Second with THE word", "Third one here.", "NaN lyric", "Last short one"],
        # 'Cleaned_Lyrics' will be generated if missing
        'Manual_Score': [0.1, 0.8, 0.5, np.nan, 0.0],
        'Labeling_Notes': ["Note1", "Note2", "Note3", "Note4", "Note5"]
    }
    df = pd.DataFrame(data)
    print("Columns in created dummy DataFrame:", df.columns.tolist())

# --- Ensure 'Cleaned_Lyrics' column exists ---
if 'Cleaned_Lyrics' not in df.columns:
    print("'Cleaned_Lyrics' column not found. Generating it from 'lyrics' column.")
    if 'lyrics' in df.columns:
        df['Cleaned_Lyrics'] = clean_lyrics_text(df['lyrics'])
        print("'Cleaned_Lyrics' column generated. Sample:")
        print(df[['lyrics', 'Cleaned_Lyrics']].head())
    else:
        print("Error: 'lyrics' column also not found. Cannot generate 'Cleaned_Lyrics'. Exiting.")
        exit()
elif df['Cleaned_Lyrics'].isnull().all() and 'lyrics' in df.columns:
    print("'Cleaned_Lyrics' column is present but all NaN. Regenerating from 'lyrics'.")
    df['Cleaned_Lyrics'] = clean_lyrics_text(df['lyrics'])
    print("'Cleaned_Lyrics' column regenerated. Sample:")
    print(df[['lyrics', 'Cleaned_Lyrics']].head())


# 3. Filter Labeled Data & Augment if necessary
if 'Manual_Score' not in df.columns:
    df['Manual_Score'] = np.nan # Should not happen if CSV loaded or dummy created ok

labeled_df = df[df['Manual_Score'].notna()].copy()

if len(labeled_df) < 3:
    print(f"Found only {len(labeled_df)} labeled samples. Augmenting for training simulation...")
    if not labeled_df.empty:
        original_labeled_count = len(labeled_df)
        while len(labeled_df) < 3:
            new_rows = labeled_df.iloc[:original_labeled_count].copy()
            new_rows['Cleaned_Lyrics'] = new_rows['Cleaned_Lyrics'].astype(str) + " copy"
            new_rows['Manual_Score'] = np.clip(new_rows['Manual_Score'] * 0.9, 0.0, 1.0)
            labeled_df = pd.concat([labeled_df, new_rows], ignore_index=True)
            if len(labeled_df) >= 3: break
    else:
        print("No labeled data found initially, creating purely dummy data for augmentation.")
        dummy_lyrics_cleaned = ["dummy lyric one", "dummy lyric two clean", "dummy lyric three four clean"]
        dummy_scores = [0.2, 0.7, 0.4]
        temp_list_of_dicts = []
        # Determine columns for the dummy DataFrame
        # If labeled_df is empty, its columns might not be set. Use df's columns.
        cols_for_dummy = df.columns if not labeled_df.empty else ['Cleaned_Lyrics', 'Manual_Score', 'Labeling_Notes'] # Add more if needed by model

        for i in range(3):
            new_row_data = {col: None for col in cols_for_dummy}
            new_row_data['Cleaned_Lyrics'] = dummy_lyrics_cleaned[i]
            new_row_data['Manual_Score'] = dummy_scores[i]
            new_row_data['Labeling_Notes'] = "Dummy augmented note"
            temp_list_of_dicts.append(new_row_data)

        current_df_for_concat = labeled_df if not labeled_df.empty and pd.DataFrame(temp_list_of_dicts).columns.equals(labeled_df.columns) else pd.DataFrame(columns=cols_for_dummy)

        if labeled_df.empty:
            labeled_df = pd.DataFrame(temp_list_of_dicts, columns=cols_for_dummy)
        else:
            # Ensure columns match before concat if labeled_df was not empty but becomes part of this.
            # This part of logic is complex due to ensuring schema match for concat.
            # Simplification: if augmentation starts from empty, just create the new one.
            pass # The initial labeled_df concat handles non-empty cases. If it was empty, it's filled above.


print(f"Total labeled samples for training: {len(labeled_df)}")
if labeled_df.empty or 'Cleaned_Lyrics' not in labeled_df.columns or labeled_df['Cleaned_Lyrics'].isnull().all():
    print("No valid 'Cleaned_Lyrics' data to train on. Exiting.")
    if not labeled_df.empty:
        print("Columns in labeled_df before exiting:", labeled_df.columns.tolist())
        print("Sample of Cleaned_Lyrics:", labeled_df['Cleaned_Lyrics'].head().tolist() if 'Cleaned_Lyrics' in labeled_df.columns else "Not found")
    exit()

# 4. Prepare Text Data
lyrics = labeled_df['Cleaned_Lyrics'].astype(str).tolist()
scores = labeled_df['Manual_Score'].values.astype(np.float32)

# 4b. Tokenizer
tokenizer = Tokenizer(num_words=5000, oov_token="<unk>")
tokenizer.fit_on_texts(lyrics)
vocabulary_size = len(tokenizer.word_index) + 1

# 4c. Convert to sequences
sequences = tokenizer.texts_to_sequences(lyrics)

# 4d. Pad sequences
maxlen = 100 # Define maxlen
padded_sequences = pad_sequences(sequences, maxlen=maxlen, padding='post', truncating='post')

X_train = padded_sequences
y_train = scores

print(f"Shape of X_train: {X_train.shape}")
print(f"Shape of y_train: {y_train.shape}")

# 6. Build LSTM Model
model = Sequential()
model.add(Embedding(input_dim=vocabulary_size, output_dim=32, input_length=maxlen))
model.add(LSTM(32))
model.add(Dense(1, activation='sigmoid'))

# 7. Compile Model
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# 8. Train Model (Simulated)
print("\nTraining model...")
batch_size = 1
if len(X_train) > 1 : batch_size = max(1, len(X_train) // 2)

history = model.fit(X_train, y_train, epochs=5, batch_size=batch_size, verbose=1)

# Print model summary
print("\nModel Summary:")
model.summary()

# Print training history
print("\nTraining History:")
if history and history.history:
    for epoch in range(len(history.history.get('loss', []))):
        loss_val = history.history['loss'][epoch]
        mae_val = history.history['mae'][epoch]
        print(f"Epoch {epoch+1}: Loss = {loss_val:.4f}, MAE = {mae_val:.4f}")
else:
    print("Training history not available.")

# 9. Save the trained model
model_path = 'data/processed/lstm_model.keras'
try:
    model.save(model_path)
    print(f"\nModel saved to {model_path}")
except Exception as e:
    print(f"\nError saving model: {e}")
