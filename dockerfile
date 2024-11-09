# Use Python 3.11 on an Alpine Linux base image for a small and efficient image
FROM python:3.11-alpine

# Set maintainer info and some metadata
LABEL maintainer="Roshan Singh" \
      description="Dockerfile for Django project using Python 3.11 and Alpine Linux" \
      version="1.0"

# Set environment variables:
# PYTHONDONTWRITEBYTECODE=1 prevents Python from writing .pyc files to the disk.
# PYTHONUNBUFFERED=1 ensures that Python output is sent straight to the terminal without buffering.
# PATH variable is updated to include the local bin directory for user-installed packages.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/django-user/.local/bin:$PATH"

# Set the working directory to /app. All subsequent commands will run from this directory.
WORKDIR /app

# Install necessary packages:
# - postgresql-client: Client for PostgreSQL databases.
# - libpq-dev: Development files for PostgreSQL, required for building Python packages that interface with PostgreSQL.
# - build-base: A meta-package that includes essential build tools.
RUN apk update && apk add --no-cache \
    postgresql-client \
    jpeg-dev \
    libpq-dev \
    build-base

# Copy the requirements files to /tmp for installing Python dependencies.
# Copying these files first helps leverage Docker layer caching and speeds up rebuilds.
COPY ./requirements.txt ./requirements.dev.txt /tmp/

# Install Python dependencies:
# - Upgrade pip to ensure the latest version is used.
# - Install dependencies listed in requirements.txt.
# - If DEV environment variable is True, also install additional development dependencies.
# - Clean up by removing the temporary requirements files to keep the image size small.
ARG DEV=False
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    [ "$DEV" = "True" ] && pip install -r /tmp/requirements.dev.txt || true && \
    rm -rf /tmp

# Copy the application code into the /app directory.
COPY project/ /app/project/
COPY apps/ /app/apps/
COPY manage.py /app/

# Create a non-root user (django-user) to run the application. This enhances security by avoiding running as root.
# Change ownership of the /app directory to this new user.
RUN adduser --disabled-password --home /home/django-user --gecos "" django-user || true && \
    chown -R django-user:django-user /app

# Expose port 8000 to allow communication to and from the Django application.
EXPOSE 8000

# Switch to the non-root user for running the Django application.
USER django-user

# Default command to run the Django development server.
# In a production environment, this would typically be replaced by a WSGI server like gunicorn.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
