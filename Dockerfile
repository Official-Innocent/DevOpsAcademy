# Start from official Python slim image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Set environment variables
ENV DEVELOPER_NAME="Innocent" \
    ENVIRONMENT="development" \
    APP_VERSION="1.0"

# Copy our script into the container
COPY app.py .

# Install any dependencies
RUN pip install psutil --break-system-packages

# What runs when container starts
CMD ["python3", "app.py"]
