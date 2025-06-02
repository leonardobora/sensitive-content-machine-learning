import re
import pandas as pd
import numpy as np
from typing import List, Tuple, Dict, Optional
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer


class LyricsPreprocessor:
    """
    Preprocessor for music lyrics to prepare data for sensitive content classification.
    """
    
    def __init__(self, model_name: str = "distilbert-base-uncased"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text for processing.
        
        Args:
            text (str): Raw lyrics text
            
        Returns:
            str: Cleaned text
        """
        if not isinstance(text, str):
            return ""
            
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        
        # Remove multiple punctuation
        text = re.sub(r'[.,!?]{2,}', '.', text)
        
        return text.strip()
    
    def tokenize_lyrics(self, lyrics: List[str], max_length: int = 512) -> Dict:
        """
        Tokenize lyrics for transformer models.
        
        Args:
            lyrics (List[str]): List of lyrics texts
            max_length (int): Maximum sequence length
            
        Returns:
            Dict: Tokenized inputs
        """
        return self.tokenizer(
            lyrics,
            truncation=True,
            padding=True,
            max_length=max_length,
            return_tensors="pt"
        )
    
    def prepare_dataset(
        self, 
        df: pd.DataFrame, 
        text_column: str = "lyrics", 
        label_column: str = "is_sensitive"
    ) -> pd.DataFrame:
        """
        Prepare dataset for training.
        
        Args:
            df (pd.DataFrame): Raw dataset
            text_column (str): Name of text column
            label_column (str): Name of label column
            
        Returns:
            pd.DataFrame: Processed dataset
        """
        # Clean text
        df = df.copy()
        df[text_column] = df[text_column].apply(self.clean_text)
        
        # Remove empty texts
        df = df[df[text_column].str.len() > 0]
        
        # Reset index
        df = df.reset_index(drop=True)
        
        return df
    
    def split_data(
        self, 
        df: pd.DataFrame,
        test_size: float = 0.2,
        val_size: float = 0.1,
        random_state: int = 42
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Split data into train, validation, and test sets.
        
        Args:
            df (pd.DataFrame): Dataset to split
            test_size (float): Test set proportion
            val_size (float): Validation set proportion
            random_state (int): Random seed
            
        Returns:
            Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: train, val, test splits
        """
        # First split: train+val vs test
        train_val, test = train_test_split(
            df, 
            test_size=test_size, 
            random_state=random_state,
            stratify=df.iloc[:, -1] if len(df.iloc[:, -1].unique()) > 1 else None
        )
        
        # Second split: train vs val
        val_size_adjusted = val_size / (1 - test_size)
        train, val = train_test_split(
            train_val,
            test_size=val_size_adjusted,
            random_state=random_state,
            stratify=train_val.iloc[:, -1] if len(train_val.iloc[:, -1].unique()) > 1 else None
        )
        
        return train, val, test
    
    def get_class_weights(self, labels: List[int]) -> Dict[int, float]:
        """
        Calculate class weights for imbalanced datasets.
        
        Args:
            labels (List[int]): List of labels
            
        Returns:
            Dict[int, float]: Class weights
        """
        from collections import Counter
        
        counter = Counter(labels)
        majority = max(counter.values())
        
        return {cls: float(majority) / count for cls, count in counter.items()}


def create_sample_dataset(n_samples: int = 100) -> pd.DataFrame:
    """
    Create a sample dataset for testing and development.
    
    Args:
        n_samples (int): Number of samples to generate
        
    Returns:
        pd.DataFrame: Sample dataset
    """
    import random
    
    # Sample lyrics (simplified for demo)
    positive_samples = [
        "love is all we need in this beautiful world",
        "dancing under the stars with my friends tonight",
        "hope springs eternal in the human heart",
        "music brings us together across all boundaries",
        "celebrating life and all its wonderful moments"
    ]
    
    negative_samples = [
        "violence and hatred consume everything around",
        "words that hurt and destroy relationships",
        "anger fills my heart with destructive thoughts",
        "negative emotions overwhelming my mind",
        "toxic behaviors affecting everyone nearby"
    ]
    
    data = []
    for i in range(n_samples):
        if random.random() < 0.3:  # 30% negative samples
            lyrics = random.choice(negative_samples)
            label = 1
        else:
            lyrics = random.choice(positive_samples)
            label = 0
            
        data.append({
            "id": i,
            "lyrics": lyrics,
            "is_sensitive": label,
            "artist": f"Artist_{i % 10}",
            "song_title": f"Song_{i}"
        })
    
    return pd.DataFrame(data)


if __name__ == "__main__":
    # Demo usage
    preprocessor = LyricsPreprocessor()
    
    # Create sample data
    df = create_sample_dataset(50)
    print(f"Created sample dataset with {len(df)} samples")
    
    # Preprocess
    df_processed = preprocessor.prepare_dataset(df)
    print(f"Processed dataset shape: {df_processed.shape}")
    
    # Split data
    train, val, test = preprocessor.split_data(df_processed)
    print(f"Split sizes - Train: {len(train)}, Val: {len(val)}, Test: {len(test)}")