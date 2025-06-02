# 🎵 Sensitive Content Classifier for Music Lyrics

A machine learning system for classifying sensitive content in music lyrics using transformer-based models.

## 🚀 Quick Start

```bash
# Setup environment
make setup

# Run the Streamlit app
make run-app
```

Visit `http://localhost:8501` to access the web interface.

## 📋 Project Overview

This project develops a machine learning system to classify sensitive content in music lyrics, identifying categories such as violence, toxic language, and other concerning material. Built with a focus on rapid development and deployment within a 15-day timeline.

### Key Features

- **🎯 Binary Classification**: Safe vs. Sensitive content detection
- **⚡ Fast Processing**: Sub-second prediction times
- **🌐 Web Interface**: User-friendly Streamlit dashboard
- **📊 Batch Analysis**: Process multiple songs at once
- **🔍 Detailed Insights**: Confidence scores and model explanations

## 🏗️ Architecture

```
src/
├── data/           # Data processing and preprocessing
├── features/       # Feature engineering
├── models/         # Model training and evaluation
└── visualization/  # Charts and plots

app/               # Streamlit web application
notebooks/         # Jupyter notebooks for exploration
tests/            # Unit and integration tests
data/             # Raw, processed, and labeled datasets
```

## 🛠️ Installation

### Requirements

- Python 3.8+
- PyTorch
- Transformers (Hugging Face)
- Streamlit

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sensitive-content-machine-learning
   ```

2. **Install dependencies**
   ```bash
   make setup
   # or manually:
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   make test
   ```

## 📖 Usage

### Web Interface

Launch the Streamlit application:

```bash
make run-app
```

The interface provides:
- **Single Prediction**: Analyze individual lyrics
- **Batch Analysis**: Upload CSV files for bulk processing
- **Model Insights**: Performance metrics and feature importance
- **Demo Data**: Sample predictions and examples

### Command Line

#### Train a Model

```bash
make train
```

#### Evaluate Model Performance

```bash
make evaluate
```

#### Process Data

```bash
make process-data
```

### Python API

```python
from src.models.model_training import SensitiveContentClassifier
from src.data.data_preprocessing import LyricsPreprocessor

# Initialize classifier
classifier = SensitiveContentClassifier()

# Make predictions
lyrics = ["Example song lyrics here"]
predictions = classifier.predict(lyrics)

print(f"Prediction: {predictions[0]['predicted_class']}")
print(f"Confidence: {predictions[0]['confidence']:.3f}")
```

## 📊 Model Details

### Base Model
- **Architecture**: DistilBERT (distilbert-base-uncased)
- **Parameters**: ~66M
- **Max Sequence Length**: 512 tokens
- **Classes**: 2 (Safe/Sensitive)

### Performance Metrics
- **Accuracy**: ~92%
- **Precision**: ~88%
- **Recall**: ~94%
- **F1-Score**: ~91%

### Training Configuration
- **Epochs**: 3
- **Batch Size**: 16
- **Learning Rate**: 2e-5
- **Optimizer**: AdamW with weight decay

## 🗂️ Data Format

### Input CSV Format
```csv
lyrics,artist,song_title
"Love is all we need in this world",Artist A,Song 1
"Violence and hatred everywhere",Artist B,Song 2
```

### Required Columns
- `lyrics`: Song lyrics text (required)
- `artist`: Artist name (optional)
- `song_title`: Song title (optional)

## 🔧 Development

### Code Quality

```bash
# Run linting
make lint

# Format code
make format

# Run tests
make test
```

### Development Cycle

```bash
# Complete development cycle
make dev
```

This runs formatting, linting, and testing in sequence.

### Adding New Features

1. **Data Processing**: Add modules to `src/data/`
2. **Model Components**: Extend `src/models/`
3. **Web Interface**: Update `app/app.py`
4. **Tests**: Add tests to `tests/`

## 🐋 Docker Support

Build and run with Docker:

```bash
# Build image
make docker-build

# Run container
make docker-run
```

## 📚 Project Structure

```
sensitive-content-machine-learning/
├── .github/workflows/     # CI/CD workflows
├── app/                   # Streamlit application
│   ├── __init__.py
│   ├── app.py            # Main app file
│   └── static/           # Static assets
├── data/                 # Data directories
│   ├── raw/              # Raw data files
│   ├── processed/        # Processed data
│   └── labeled/          # Labeled datasets
├── docs/                 # Documentation
├── notebooks/            # Jupyter notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_model_evaluation.ipynb
├── src/                  # Source code
│   ├── data/             # Data processing
│   ├── features/         # Feature engineering
│   ├── models/           # ML models
│   └── visualization/    # Plotting utilities
├── tests/                # Test suite
├── .gitignore
├── Makefile              # Build automation
├── README.md
└── requirements.txt      # Dependencies
```

## 🎯 Roadmap

### MVP (Current Phase)
- [x] Basic binary classification (Safe/Sensitive)
- [x] Streamlit web interface
- [x] DistilBERT-based model
- [x] Batch processing capability

### Future Enhancements
- [ ] Multi-label classification (Violence, Hate Speech, etc.)
- [ ] Model explainability (LIME/SHAP integration)
- [ ] REST API for integration
- [ ] Real-time streaming analysis
- [ ] Advanced visualization dashboard

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation as needed
- Use type hints where applicable

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hugging Face Transformers** for the model architecture
- **Streamlit** for the web interface framework
- **PyTorch** for the deep learning backend

## 📞 Support

For questions, issues, or contributions:

- 📧 Create an issue in this repository
- 📖 Check the documentation in `docs/`
- 💬 Join our development discussions

---

**⚠️ Disclaimer**: This tool is designed to assist in content classification but should not be the sole method for content moderation decisions. Human review is recommended for critical applications.