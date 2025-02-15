# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Install Node.js and Prettier ---
RUN apt-get update && apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g prettier@3.4.2 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the agent code into the container
COPY agent/ ./agent/

# Expose port 8000 for the API
EXPOSE 8000

# Run the application using uvicorn
CMD ["uvicorn", "agent.main:app", "--host", "0.0.0.0", "--port", "8000"]

