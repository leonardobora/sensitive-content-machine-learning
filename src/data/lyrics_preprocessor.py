import pandas as pd
import numpy as np
import re
from pathlib import Path
from sklearn.model_selection import train_test_split
import json

class LyricsPreprocessor:
    """Preprocessing pipeline for song lyrics data with sensitive content detection."""
    
    def __init__(self, raw_data_path=None):
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.raw_data_path = raw_data_path or self.data_dir / "raw" / "songs_lyrics_dataset.csv"
        self.processed_data_path = self.data_dir / "processed"
        self.processed_data_path.mkdir(exist_ok=True)
        
        # Define sensitive content categories
        self.sensitive_categories = {
            'explicit_language': [
                'fuck', 'shit', 'damn', 'hell', 'bitch', 'ass', 'bastard',
                'cock', 'dick', 'pussy', 'whore', 'slut', 'motherfucker'
            ],
            'violence': [
                'kill', 'murder', 'blood', 'death', 'gun', 'knife', 'fight',
                'shoot', 'stab', 'beat', 'punch', 'violence', 'war', 'battle'
            ],
            'sexual_content': [
                'sex', 'sexual', 'bedroom', 'naked', 'strip', 'seduce',
                'erotic', 'intimate', 'pleasure', 'desire', 'lust'
            ],
            'substance_abuse': [
                'drug', 'cocaine', 'weed', 'marijuana', 'alcohol', 'drunk',
                'high', 'smoke', 'drink', 'bottle', 'beer', 'wine', 'whiskey'
            ]
        }
    
    def load_data(self):
        """Load raw dataset."""
        try:
            df = pd.read_csv(self.raw_data_path)
            print("Data loaded successfully. Shape: {}".format(df.shape))
            return df
        except Exception as e:
            print("Error loading data: {}".format(e))
            raise
    
    def clean_text(self, text):
        """Clean and normalize text data."""
        if pd.isna(text):
            return ""
        
        # Convert to lowercase
        text = str(text).lower()
        
        # Remove special characters but keep spaces and basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def detect_sensitive_content(self, lyrics):
        """Detect sensitive content categories in lyrics."""
        if pd.isna(lyrics):
            return []
        
        lyrics_clean = self.clean_text(lyrics)
        detected_categories = []
        
        for category, keywords in self.sensitive_categories.items():
            if any(keyword in lyrics_clean for keyword in keywords):
                detected_categories.append(category)
        
        return detected_categories
    
    def create_labels(self, df):
        """Create binary labels for sensitive content categories."""
        print("Creating labels for sensitive content detection...")
        
        # Apply sensitive content detection
        df['sensitive_categories'] = df['Lyrics'].apply(self.detect_sensitive_content)
        
        # Create binary columns for each category
        for category in self.sensitive_categories.keys():
            df[category] = df['sensitive_categories'].apply(
                lambda x: 1 if category in x else 0
            )
        
        # Create overall sensitive content flag
        df['has_sensitive_content'] = df['sensitive_categories'].apply(
            lambda x: 1 if len(x) > 0 else 0
        )
        
        return df
    
    def preprocess_features(self, df):
        """Preprocess text features and create additional features."""
        print("Preprocessing features...")
        
        # Clean lyrics text
        df['lyrics_clean'] = df['Lyrics'].apply(self.clean_text)
        
        # Create text statistics features
        df['lyrics_length'] = df['lyrics_clean'].apply(len)
        df['word_count'] = df['lyrics_clean'].apply(lambda x: len(x.split()) if x else 0)
        df['unique_word_ratio'] = df.apply(
            lambda row: len(set(row['lyrics_clean'].split())) / max(row['word_count'], 1)
            if row['lyrics_clean'] else 0, axis=1
        )
        
        # Clean and encode categorical features
        df['artist_clean'] = df['Artist'].fillna('unknown')
        df['year_decade'] = (df['Year'] // 10) * 10
        
        return df
    
    def split_data(self, df, test_size=0.2, val_size=0.1):
        """Split data into train, validation, and test sets."""
        print("Splitting data into train/val/test sets...")
        
        # Features and targets
        feature_columns = ['lyrics_clean', 'lyrics_length', 'word_count', 
                          'unique_word_ratio', 'Year', 'year_decade']
        target_columns = ['has_sensitive_content'] + list(self.sensitive_categories.keys())
        
        X = df[feature_columns].copy()
        y = df[target_columns].copy()
        
        # First split: train+val and test
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y['has_sensitive_content']
        )
        
        # Second split: train and val
        val_size_adjusted = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_size_adjusted, random_state=42, 
            stratify=y_temp['has_sensitive_content']
        )
        
        print("Train set: {} samples".format(len(X_train)))
        print("Validation set: {} samples".format(len(X_val)))
        print("Test set: {} samples".format(len(X_test)))
        
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def save_processed_data(self, X_train, X_val, X_test, y_train, y_val, y_test):
        """Save processed datasets to files."""
        print("Saving processed data...")
        
        # Combine features and targets for saving
        train_data = pd.concat([X_train, y_train], axis=1)
        val_data = pd.concat([X_val, y_val], axis=1)
        test_data = pd.concat([X_test, y_test], axis=1)
        
        # Save to CSV
        train_data.to_csv(self.processed_data_path / "train.csv", index=False)
        val_data.to_csv(self.processed_data_path / "val.csv", index=False)
        test_data.to_csv(self.processed_data_path / "test.csv", index=False)
        
        # Save metadata
        metadata = {
            'feature_columns': list(X_train.columns),
            'target_columns': list(y_train.columns),
            'sensitive_categories': self.sensitive_categories,
            'train_size': len(X_train),
            'val_size': len(X_val),
            'test_size': len(X_test)
        }
        
        with open(self.processed_data_path / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print("Data saved to: {}".format(self.processed_data_path))
        
        return metadata
    
    def run_preprocessing(self):
        """Run complete preprocessing pipeline."""
        print("Starting preprocessing pipeline...")
        
        # Load data
        df = self.load_data()
        
        # Create labels
        df = self.create_labels(df)
        
        # Preprocess features
        df = self.preprocess_features(df)
        
        # Split data
        X_train, X_val, X_test, y_train, y_val, y_test = self.split_data(df)
        
        # Save processed data
        metadata = self.save_processed_data(X_train, X_val, X_test, y_train, y_val, y_test)
        
        # Print summary statistics
        print("\n=== Preprocessing Summary ===")
        print("Total samples: {}".format(len(df)))
        print("Sensitive content distribution:")
        for category in self.sensitive_categories.keys():
            count = df[category].sum()
            percentage = (count / len(df)) * 100
            print("  {}: {} ({:.1f}%)".format(category, count, percentage))
        
        overall_sensitive = df['has_sensitive_content'].sum()
        print("Overall sensitive content: {} ({:.1f}%)".format(
            overall_sensitive, (overall_sensitive / len(df)) * 100
        ))
        
        return df, metadata

if __name__ == "__main__":
    preprocessor = LyricsPreprocessor()
    df, metadata = preprocessor.run_preprocessing()