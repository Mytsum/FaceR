FROM python:3.9-slim

# Install build tools and dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libboost-python-dev \
    libboost-thread-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    wget

# Install dlib
RUN pip install dlib

# Install other Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY . /app
WORKDIR /app

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]