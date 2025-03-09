FROM python:3.9

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set environment variable to force TensorFlow to use CPU


# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirments.txt



# Copy the application code
COPY . .

# Expose necessary ports
EXPOSE 8000

# Start the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
