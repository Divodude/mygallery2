# Use Python 3.9 as the base image
FROM python:3.9

# Install system dependencies
#RUN apt-get update && apt-get install -y \
#    libgl1-mesa-glx \
#    libglib2.0-0 \
#    ffmpeg \
#    && rm -rf /var/lib/apt/lists/*

# Set environment variable to force TensorFlow to use CPU (if needed)
# ENV TF_ENABLE_ONEDNN_OPTS=0

# Set working directory inside the container
WORKDIR /app

# Copy requirements first (to leverage Docker caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port for the application
EXPOSE 8000

# Start the application with Gunicorn
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

