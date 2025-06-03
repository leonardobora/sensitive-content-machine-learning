# Technical Report: Analysis of Potentially Inappropriate Content in Song Lyrics (1950-2019)

## 1. Introduction
    - **Project Goals**: To develop a system for identifying and analyzing potentially inappropriate content in song lyrics from a historical dataset.
    - **Scope**:
        - Utilizing a dataset of song lyrics spanning from 1950 to 2019.
        - Focusing on text-based analysis of lyrics.
        - Developing a preliminary model for scoring lyrics based on simulated manual labels.
        - Conducting exploratory analysis on trends and characteristics of high-scoring songs.
    - **Target Audience**: Academic researchers, cultural analysts, music industry professionals interested in content trends.

## 2. Methodology

### 2.1. Dataset Description
    - **Source**: Kaggle Dataset "Music Dataset 1950 to 2019" (specifically `all_songs_data_processed.csv`). (Note: Actual download was simulated with dummy data due to access restrictions).
    - **Key Features**: Track ID, artist name, track name, release date, genre, lyrics, tempo, danceability, etc.
    - **Initial Exploration Findings**:
        - Brief overview of data structure (e.g., number of songs, time span covered by the dummy data).
        - Distribution of songs over years (if available from dummy data exploration).
        - Initial look at lyric length or other relevant text features from the dummy data.
        - (Reference: Initial data loading and `df.info()`, `df.head()` from Subtask 1).

### 2.2. Data Preprocessing
    - **Text Cleaning**:
        - Conversion to lowercase.
        - Removal of punctuation.
        - Removal of common English stopwords (NLTK library).
        - Creation of a 'Cleaned_Lyrics' column.
        - (Reference: Text preprocessing script from Subtask 2).
    - **Handling Missing Data**:
        - Discussion of how missing 'lyrics' or 'Cleaned_Lyrics' were handled (e.g., filled with empty strings for processing).
        - Impact on analysis or modeling.

### 2.3. Manual Labeling Simulation
    - **Objective**: To create a small, labeled subset for initial model training, simulating a manual review process.
    - **Criteria (Hypothetical for this project)**:
        - Defining categories of potentially inappropriate content (e.g., explicit language, violence, hate speech, suggestive content).
        - Development of a scoring rubric (e.g., 0.0 to 1.0 scale for severity).
    - **Process**:
        - A small subset of songs (first 3 rows of the dummy dataset) was manually assigned scores (`Manual_Score`) and qualitative notes (`Labeling_Notes`).
        - (Reference: Manual labeling simulation script from Subtask 3).
    - **Offensive Terms Dictionary**:
        - A placeholder dictionary (`data/labeled/offensive_terms_dictionary.txt`) was created with example terms.
        - Intended use: Could assist manual labelers or be a basis for future feature engineering (not used in the current LSTM model directly).
        - (Reference: `offensive_terms_dictionary.txt` created in Subtask 3).

### 2.4. Modeling Approach
    - **Choice of Model**: Long Short-Term Memory (LSTM) network, suitable for sequence data like text.
    - **Input Features**: Tokenized and padded sequences derived from 'Cleaned_Lyrics'.
    - **Target Variable**: 'Manual_Score' (float).
    - **Architecture Details**:
        - Embedding Layer (Input dimension based on vocabulary size from training tokenizer, output dimension e.g., 32).
        - LSTM Layer (e.g., 32 units).
        - Dense Output Layer (1 unit, 'sigmoid' activation for scores between 0 and 1).
        - (Reference: Model training script from Subtask 4, `lstm_model.keras`).
    - **Training Process**:
        - Tokenizer fitted on the 'Cleaned_Lyrics' of the small labeled training set.
        - Model compiled with Adam optimizer, Mean Squared Error (MSE) loss, and Mean Absolute Error (MAE) metric.
        - Trained for a small number of epochs (e.g., 5) on the limited labeled data.
        - (Reference: Model training script from Subtask 4).

## 3. Results and Analysis

### 3.1. Model Performance (Simulated)
    - **Evaluation Metrics**: MSE and MAE from the training phase on the very small dataset.
    - **Limitations**:
        - Due to the extremely small size and nature of the simulated labeled dataset (3 samples), these metrics are not indicative of real-world performance.
        - No separate test/validation set was used in this simulation.
        - Acknowledge that robust evaluation would require a much larger and more diverse labeled dataset.

### 3.2. Temporal Analysis (Based on Predictions on Full Dummy Dataset)
    - **Trend Visualization**: Average 'Predicted_Score' grouped by 'Year'.
    - **Interpretation**: Discuss any observed patterns (e.g., increase/decrease in predicted scores over time periods represented in the dummy data).
    - **Caveats**: Emphasize that these trends are based on a model trained on very limited, simulated data and may not reflect actual historical trends.
    - (Reference: Prediction and analysis script from Subtask 5, `songs_with_predictions.csv`).

### 3.3. Content Analysis (Based on Predictions on Full Dummy Dataset)
    - **Ranking of Unlabeled Songs**: Top 5 songs with the highest 'Predicted_Score'.
    - **Characteristics of High-Scoring Songs (Qualitative based on dummy data)**: If possible, briefly examine the 'lyrics' or 'Cleaned_Lyrics' of these top songs from the dummy data to see if the model is picking up on any (coincidental) patterns.
    - (Reference: Prediction and analysis script from Subtask 5, `songs_with_predictions.csv`).

## 4. Ethical and Technical Limitations
    - **Bias in Data and Labels**:
        - The original Kaggle dataset may have inherent biases (e.g., genre representation, regional focus).
        - The simulated manual labeling is subjective and not based on rigorous, validated criteria. A real project would require a detailed annotation guide and inter-annotator agreement checks.
    - **Model Interpretability**: LSTMs can be black boxes; understanding *why* a song gets a high score can be challenging.
    - **Contextual Understanding**: Text-only analysis misses crucial context from audio, artist intent, cultural nuances, and slang evolution.
    - **Definition of "Inappropriate"**: Highly subjective and culturally dependent. This project uses a simulated definition.
    - **Oversimplification**: The current model is very basic and trained on minimal data. It serves as a proof-of-concept for the workflow rather than a reliable tool for content moderation.
    - **Dynamic Nature of Language**: Slang and offensive terms change over time; a static dictionary or model may become outdated.

## 5. Conclusion
    - **Summary of Work**: Briefly reiterate the steps taken (data prep, simulated labeling, model training, prediction).
    - **Key (Simulated) Insights**: Mention the feasibility of the workflow and the types of analysis possible (temporal, content-based ranking), even with dummy/limited data.
    - **Limitations Recap**: Re-emphasize the preliminary nature of the findings.
    - **Future Work**:
        - Acquiring and robustly labeling a larger dataset.
        - Exploring more sophisticated models (e.g., Transformers, incorporating metadata).
        - Developing a more nuanced and validated set of labeling criteria.
        - Incorporating techniques for model interpretability.
        - User interface for exploring results.

## 6. References
    - All sources cited in the report will be listed here.
    - Formatting will follow ABNT (Associação Brasileira de Normas Técnicas) standards. (e.g., NLTK library, TensorFlow, Pandas, original dataset source).
