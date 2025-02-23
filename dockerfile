# Use the official Python 3.11 base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy local project files into the container (if any exist yet)
COPY . /app

# Install system dependencies (optional)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential

# Upgrade pip (optional)
RUN pip install --no-cache-dir --upgrade pip

# Default command to keep the container running or open a shell
CMD ["bash"]
