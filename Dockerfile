# Base image
FROM python:3.13-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_ROOT_USER_ACTION=ignore

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    build-base \
    postgresql-dev \
    libaio \
    wget \
    unzip

# Install Poetry
RUN pip install --no-cache-dir uv

# Copy Python dependency management files
COPY pyproject.toml uv.lock /app/

# Install Python dependencies without virtual environment
RUN uv sync --no-dev

# Copy the project files to the container
COPY . /app/

# Expose the port that the Django app runs on
EXPOSE 8080

# Run the Django development server
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8080"]
