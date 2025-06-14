# syntax=docker/dockerfile:1
# Use an official Python runtime as a parent image
FROM --platform=$BUILDPLATFORM python:3.11-slim
# Build for the detected build platform but image will be portable to TARGETPLATFORM

# Metadata showing the build and target architecture
ARG BUILDPLATFORM
ARG TARGETPLATFORM
# Set PYTHONUNBUFFERED to get logs straight away
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Default command to run the bot
CMD ["python", "bot.py"]
