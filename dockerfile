# Base image, why better than ubuntu?
FROM python:3.9

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the Flask app files
COPY . .

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Read access token from file and set as environment variable
RUN ACCESS_TOKEN=$(cat access_token.txt) && \
    echo "TRANSFORMERS_ACCESS_TOKEN=$ACCESS_TOKEN" >> /etc/environment

# Expose the Flask port
EXPOSE 5000

# Entrypoint command to start the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
