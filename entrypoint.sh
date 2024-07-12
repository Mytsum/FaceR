#!/bin/bash
set -e

echo "Starting application..."

# Run any necessary pre-start commands here

# Start the application
exec uvicorn main:app --host 0.0.0.0 --port 8000
