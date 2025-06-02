# Sensitive Content ML Project Makefile

.PHONY: help setup install dev-install lint test train evaluate clean run-app docker-build docker-run

# Default target
help:
	@echo "Available commands:"
	@echo "  setup          - Set up the development environment"
	@echo "  install        - Install production dependencies"
	@echo "  dev-install    - Install development dependencies"
	@echo "  lint           - Run code linting"
	@echo "  format         - Format code with black and isort"
	@echo "  test           - Run tests"
	@echo "  train          - Train the model"
	@echo "  evaluate       - Evaluate the model"
	@echo "  run-app        - Run the Streamlit application"
	@echo "  clean          - Clean temporary files"
	@echo "  docker-build   - Build Docker image"
	@echo "  docker-run     - Run Docker container"

# Environment setup
setup: install
	@echo "Setting up development environment..."
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	@echo "Setup complete!"

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

dev-install: install
	@echo "Installing development dependencies..."
	pip install pytest flake8 black isort jupyter

# Code quality
lint:
	@echo "Running linting..."
	flake8 src/ app/ --max-line-length=88 --extend-ignore=E203,W503
	@echo "Linting complete!"

format:
	@echo "Formatting code..."
	black src/ app/ --line-length=88
	isort src/ app/ --profile=black
	@echo "Formatting complete!"

# Testing
test:
	@echo "Running tests..."
	python -m pytest tests/ -v
	@echo "Tests complete!"

# Model operations
train:
	@echo "Training model..."
	python -m src.models.model_training
	@echo "Training complete!"

evaluate:
	@echo "Evaluating model..."
	python -m src.models.model_evaluation
	@echo "Evaluation complete!"

# Data operations
process-data:
	@echo "Processing data..."
	python -m src.data.data_preprocessing
	@echo "Data processing complete!"

# Application
run-app:
	@echo "Starting Streamlit application..."
	streamlit run app/app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true

run-local:
	@echo "Starting local development server..."
	python -m http.server 8000

# Cleanup
clean:
	@echo "Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@echo "Cleanup complete!"

# Docker operations
docker-build:
	@echo "Building Docker image..."
	docker build -t sensitive-content-ml .

docker-run:
	@echo "Running Docker container..."
	docker run -p 8501:8501 sensitive-content-ml

# Development helpers
jupyter:
	@echo "Starting Jupyter notebook server..."
	jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root

# CI/CD helpers
ci: lint test
	@echo "CI pipeline complete!"

all: setup lint test train
	@echo "All tasks complete!"

# Quick development cycle
dev: format lint test
	@echo "Development cycle complete!"