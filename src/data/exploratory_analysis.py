import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
from collections import Counter
import re

class DataExplorer:
    """Exploratory data analysis for sensitive content lyrics dataset."""
    
    def __init__(self, processed_data_path=None):
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.processed_data_path = processed_data_path or self.data_dir / "processed"
        self.figures_dir = self.data_dir / "figures"
        self.figures_dir.mkdir(exist_ok=True)
        
        # Load metadata
        with open(self.processed_data_path / "metadata.json", 'r') as f:
            self.metadata = json.load(f)
    
    def load_processed_data(self):
        """Load processed datasets."""
        train_data = pd.read_csv(self.processed_data_path / "train.csv")
        val_data = pd.read_csv(self.processed_data_path / "val.csv")
        test_data = pd.read_csv(self.processed_data_path / "test.csv")
        
        # Combine for overall analysis
        full_data = pd.concat([train_data, val_data, test_data], ignore_index=True)
        
        return {
            'train': train_data,
            'val': val_data,
            'test': test_data,
            'full': full_data
        }
    
    def dataset_overview(self, datasets):
        """Print basic dataset statistics."""
        print("=== Dataset Overview ===")
        
        for name, data in datasets.items():
            if name == 'full':
                continue
            print("{}:".format(name.capitalize()))
            print("  Shape: {}".format(data.shape))
            print("  Sensitive content ratio: {:.2f}%".format(
                data['has_sensitive_content'].mean() * 100
            ))
        
        print("\nFull Dataset:")
        print("  Total samples: {}".format(len(datasets['full'])))
        print("  Features: {}".format(len(self.metadata['feature_columns'])))
        print("  Target categories: {}".format(len(self.metadata['target_columns'])))
    
    def analyze_sensitive_content_distribution(self, data):
        """Analyze distribution of sensitive content categories."""
        print("\n=== Sensitive Content Distribution ===")
        
        target_columns = [col for col in self.metadata['target_columns'] 
                         if col != 'has_sensitive_content']
        
        # Calculate statistics for each category
        stats = {}
        for category in target_columns:
            count = data[category].sum()
            percentage = (count / len(data)) * 100
            stats[category] = {'count': count, 'percentage': percentage}
            print("{}: {} samples ({:.1f}%)".format(category, count, percentage))
        
        # Overall sensitive content
        overall_count = data['has_sensitive_content'].sum()
        overall_percentage = (overall_count / len(data)) * 100
        print("Overall sensitive: {} samples ({:.1f}%)".format(
            overall_count, overall_percentage
        ))
        
        return stats
    
    def analyze_text_statistics(self, data):
        """Analyze text length and word count statistics."""
        print("\n=== Text Statistics ===")
        
        # Text length statistics
        print("Lyrics length (characters):")
        print("  Mean: {:.1f}".format(data['lyrics_length'].mean()))
        print("  Median: {:.1f}".format(data['lyrics_length'].median()))
        print("  Min: {}".format(data['lyrics_length'].min()))
        print("  Max: {}".format(data['lyrics_length'].max()))
        
        # Word count statistics
        print("\nWord count:")
        print("  Mean: {:.1f}".format(data['word_count'].mean()))
        print("  Median: {:.1f}".format(data['word_count'].median()))
        print("  Min: {}".format(data['word_count'].min()))
        print("  Max: {}".format(data['word_count'].max()))
        
        # Unique word ratio
        print("\nUnique word ratio:")
        print("  Mean: {:.3f}".format(data['unique_word_ratio'].mean()))
        print("  Median: {:.3f}".format(data['unique_word_ratio'].median()))
        
        return {
            'lyrics_length': data['lyrics_length'].describe(),
            'word_count': data['word_count'].describe(),
            'unique_word_ratio': data['unique_word_ratio'].describe()
        }
    
    def analyze_temporal_trends(self, data):
        """Analyze trends over time."""
        print("\n=== Temporal Analysis ===")
        
        # Group by decade
        decade_stats = data.groupby('year_decade').agg({
            'has_sensitive_content': ['count', 'sum', 'mean'],
            'lyrics_length': 'mean',
            'word_count': 'mean'
        }).round(3)
        
        print("Trends by decade:")
        print(decade_stats)
        
        return decade_stats
    
    def find_common_words(self, data, category=None, top_n=20):
        """Find most common words in lyrics, optionally filtered by category."""
        print("\n=== Common Words Analysis ===")
        
        # Filter data if category is specified
        if category:
            if category in data.columns:
                filtered_data = data[data[category] == 1]
                print("Top {} words in '{}' category:".format(top_n, category))
            else:
                print("Category '{}' not found.".format(category))
                return
        else:
            filtered_data = data
            print("Top {} words overall:".format(top_n))
        
        # Combine all lyrics
        all_lyrics = ' '.join(filtered_data['lyrics_clean'].fillna(''))
        
        # Split into words and count
        words = re.findall(r'\b\w+\b', all_lyrics.lower())
        word_counts = Counter(words)
        
        # Remove very common words (basic stopwords)
        stopwords = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 
                    'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                    'could', 'should', 'may', 'might', 'must', 'can', 'a', 'an',
                    'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she',
                    'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        
        filtered_counts = {word: count for word, count in word_counts.items() 
                          if word not in stopwords and len(word) > 2}
        
        # Get top words
        top_words = Counter(filtered_counts).most_common(top_n)
        
        for word, count in top_words:
            print("  {}: {}".format(word, count))
        
        return top_words
    
    def create_visualizations(self, data):
        """Create and save visualization plots."""
        print("\n=== Creating Visualizations ===")
        
        plt.style.use('default')
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Sensitive Content Analysis - Dataset Overview', fontsize=16)
        
        # 1. Sensitive content distribution
        target_columns = [col for col in self.metadata['target_columns'] 
                         if col != 'has_sensitive_content']
        counts = [data[col].sum() for col in target_columns]
        
        axes[0, 0].bar(target_columns, counts, color='steelblue')
        axes[0, 0].set_title('Sensitive Content Categories')
        axes[0, 0].set_ylabel('Count')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # 2. Text length distribution
        axes[0, 1].hist(data['lyrics_length'], bins=50, alpha=0.7, color='green')
        axes[0, 1].set_title('Distribution of Lyrics Length')
        axes[0, 1].set_xlabel('Characters')
        axes[0, 1].set_ylabel('Frequency')
        
        # 3. Word count distribution
        axes[0, 2].hist(data['word_count'], bins=50, alpha=0.7, color='orange')
        axes[0, 2].set_title('Distribution of Word Count')
        axes[0, 2].set_xlabel('Words')
        axes[0, 2].set_ylabel('Frequency')
        
        # 4. Sensitive vs non-sensitive comparison
        sensitive_lengths = data[data['has_sensitive_content'] == 1]['lyrics_length']
        non_sensitive_lengths = data[data['has_sensitive_content'] == 0]['lyrics_length']
        
        axes[1, 0].hist([sensitive_lengths, non_sensitive_lengths], 
                       bins=30, alpha=0.7, label=['Sensitive', 'Non-sensitive'],
                       color=['red', 'blue'])
        axes[1, 0].set_title('Lyrics Length by Sensitivity')
        axes[1, 0].set_xlabel('Characters')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].legend()
        
        # 5. Temporal trends
        decade_means = data.groupby('year_decade')['has_sensitive_content'].mean()
        axes[1, 1].plot(decade_means.index, decade_means.values, marker='o', linewidth=2)
        axes[1, 1].set_title('Sensitive Content Trend by Decade')
        axes[1, 1].set_xlabel('Decade')
        axes[1, 1].set_ylabel('Proportion of Sensitive Content')
        axes[1, 1].grid(True, alpha=0.3)
        
        # 6. Category correlation heatmap
        category_corr = data[target_columns].corr()
        im = axes[1, 2].imshow(category_corr, cmap='coolwarm', aspect='auto')
        axes[1, 2].set_title('Category Correlation Heatmap')
        axes[1, 2].set_xticks(range(len(target_columns)))
        axes[1, 2].set_yticks(range(len(target_columns)))
        axes[1, 2].set_xticklabels(target_columns, rotation=45)
        axes[1, 2].set_yticklabels(target_columns)
        
        # Add colorbar
        plt.colorbar(im, ax=axes[1, 2])
        
        plt.tight_layout()
        
        # Save plot
        plot_path = self.figures_dir / "data_exploration.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print("Visualizations saved to: {}".format(plot_path))
        
        plt.show()
    
    def run_full_analysis(self):
        """Run complete exploratory data analysis."""
        print("Starting exploratory data analysis...")
        
        # Load data
        datasets = self.load_processed_data()
        data = datasets['full']
        
        # Run analyses
        self.dataset_overview(datasets)
        
        sensitive_stats = self.analyze_sensitive_content_distribution(data)
        
        text_stats = self.analyze_text_statistics(data)
        
        temporal_stats = self.analyze_temporal_trends(data)
        
        # Word analysis for different categories
        self.find_common_words(data, top_n=15)
        self.find_common_words(data, 'explicit_language', top_n=10)
        self.find_common_words(data, 'violence', top_n=10)
        
        # Create visualizations
        self.create_visualizations(data)
        
        return {
            'datasets': datasets,
            'sensitive_stats': sensitive_stats,
            'text_stats': text_stats,
            'temporal_stats': temporal_stats
        }

if __name__ == "__main__":
    explorer = DataExplorer()
    results = explorer.run_full_analysis()