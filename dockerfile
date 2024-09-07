FROM python:3.11-alpine

# Set maintainer info and some metadata
LABEL maintainer="Roshan Singh" \
      description="Dockerfile for Django project using Python 3.11 and Alpine Linux" \
      version="1.0"

# Set environment variables to prevent Python from writing pyc files and ensure logs are unbuffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/django-user/.local/bin:$PATH"

# Set /app as the working directory. All subsequent commands will operate here.
WORKDIR /app

# Install system dependencies in one go to minimize image layers.
RUN apk update && apk add --no-cache \
    gcc musl-dev postgresql-dev libffi-dev python3-dev build-base bash && \
    # Clean up apk cache to reduce image size
    rm -rf /var/cache/apk/*

# Copy requirements files first to leverage Docker layer caching.
COPY ./requirements.txt ./requirements.dev.txt /tmp/

# Install Python dependencies and upgrade pip in one go to avoid creating multiple layers.
ARG DEV=False
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    [ "$DEV" = "True" ] && pip install -r /tmp/requirements.dev.txt || true && \
    # Remove the temporary requirements files to keep the image clean and small
    rm -rf /tmp

# Copy the actual application code (Django project and apps) into the working directory.
COPY project/ /app/project/
COPY apps/ /app/apps/
COPY manage.py /app/

# Create a non-root user (django-user) to avoid running the app as root, which is a security risk.
RUN adduser --disabled-password --home /home/django-user --gecos "" django-user || true && \
    # Ensure the new user has ownership of the app files
    chown -R django-user:django-user /app

# Expose the port where the Django app will run (default is 8000 for development)
EXPOSE 8000

# Switch to the non-root user for running the Django app. This improves security.
USER django-user

# Use the built-in Django development server for now. In production, you'd likely switch to something like gunicorn.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
