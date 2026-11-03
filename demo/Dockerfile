# Use python runtime as base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV AUTHOR="Mesake"

# Set the working directory in the container
WORKDIR /app

# Install system packages required by Wagtail / Pillow
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

USER root
# # Create user and group for running the application
# RUN groupadd -r appuser && useradd -r -g appuser appuser
# # Change ownership of the application files to the new user
# RUN chown -R appuser:appuser /app

# # Switch to the new user
# USER appuser

# Entry point for the wagtail application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]
