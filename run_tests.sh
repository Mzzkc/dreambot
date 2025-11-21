#!/bin/bash
# Test runner script for dreambot

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Set PYTHONPATH to include src directory
export PYTHONPATH=/home/emzi/Projects/dreambot/src

# Run pytest with verbose output
pytest tests/ -v "$@"
