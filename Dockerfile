# Use an official Python runtime as a parent image
FROM python:3.11-slim-bookworm

# Copy --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

# Set work directory
WORKDIR /app

# Install system dependencies (if needed for psycopg or other libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
# --frozen ensures we use exactly what is in uv.lock
RUN uv sync --frozen --no-dev

# Copy the rest of the application
COPY . .

# Make sure the virtual environment created by uv is on the PATH
# uv creates the venv in .venv by default
ENV PATH="/app/.venv/bin:$PATH"

# Run the application
# We use a shell script or direct command. 
# Here we run migrations and then start the server.
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:80"]