#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Train the model so the dashboard has the necessary .pkl files
python -m src.predictor.train
