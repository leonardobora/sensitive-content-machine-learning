# Code References for Project Notebook/Submission

This document lists the key Python scripts and logic blocks developed throughout the project subtasks. These would be organized and adapted into a final code submission, likely as a main Jupyter Notebook or a set of structured Python files.

## 1. Data Loading and Initial Setup (Corresponds to Subtask 1)
- **Script/Logic**: Initial loading of `all_songs_data_processed.csv` (or its dummy equivalent).
- **Functionality**: Using pandas to read CSV, `df.head()`, `df.info()` for initial data overview.
- **File**: Part of the Python script in `run_in_bash_session` from Subtask 1.

## 2. Text Preprocessing (Corresponds to Subtask 2)
- **Script/Logic**: Python script for cleaning the 'lyrics' column.
- **Functionality**:
    - Lowercasing text.
    - Removing punctuation (`string.punctuation`).
    - Removing stopwords (`nltk.corpus.stopwords`, `nltk.tokenize.word_tokenize`).
    - Storing results in 'Cleaned_Lyrics'.
    - Handling missing values in 'lyrics' before cleaning.
- **File**: `process_lyrics.py` (or equivalent) created via `cat << EOF` in `run_in_bash_session` from Subtask 2.

## 3. Manual Labeling Simulation & Dictionary Creation (Corresponds to Subtask 3)
- **Script/Logic**: Python script for adding manual labels and notes to a subset of data.
- **Functionality**:
    - Adding `Manual_Score` and `Labeling_Notes` columns.
    - Populating these for the first 3 rows.
    - Saving to `data/labeled/manually_labeled_songs.csv`.
- **File**: `process_and_label.py` (or equivalent) from Subtask 3.
- **Associated File**: `data/labeled/offensive_terms_dictionary.txt` (content generation).

## 4. LSTM Model Training (Corresponds to Subtask 4)
- **Script/Logic**: Python script for building and training the LSTM model.
- **Functionality**:
    - Loading `manually_labeled_songs.csv`.
    - Filtering/augmenting labeled data.
    - Text vectorization: `tensorflow.keras.preprocessing.text.Tokenizer`, `pad_sequences`.
    - LSTM model definition: `Sequential` API with `Embedding`, `LSTM`, `Dense` layers.
    - Model compilation (`optimizer='adam'`, `loss='mse'`).
    - Model training (`model.fit()`).
    - Saving the model (`model.save('data/processed/lstm_model.keras')`).
- **File**: `train_model.py` (or equivalent) from Subtask 4.

## 5. Prediction and Analysis (Corresponds to Subtask 5)
- **Script/Logic**: Python script for loading the trained model and making predictions on the full dataset.
- **Functionality**:
    - Loading the saved LSTM model (`load_model`).
    - Re-fitting/aligning tokenizer with the model's training vocabulary.
    - Loading `all_songs_data_processed.csv`.
    - Ensuring 'Cleaned_Lyrics' exists (regenerating if necessary).
    - Preparing sequences for the full dataset.
    - Making predictions (`model.predict()`).
    - Adding 'Predicted_Score' to DataFrame.
    - Basic analysis: Top 5 songs, average score per year.
    - Saving results to `data/processed/songs_with_predictions.csv`.
- **File**: `predict_and_analyze.py` (or equivalent) from Subtask 5.

## Final Code Structure
For the final project submission, these individual scripts and logic pieces would be integrated into:
- A comprehensive Jupyter Notebook demonstrating the end-to-end workflow with explanations and visualizations.
- Alternatively, a set of modular Python (.py) files organized by functionality (e.g., `data_loader.py`, `preprocessing.py`, `model.py`, `train.py`, `predict.py`, `main_notebook.ipynb`).

This approach ensures reproducibility and a clear presentation of the project's development.
