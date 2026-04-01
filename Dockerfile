FROM python:3.12-slim

# Install Node.js
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install backend deps
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Install frontend deps and build
COPY frontend/package.json frontend/package-lock.json frontend/
RUN cd frontend && npm ci

COPY frontend/ frontend/
RUN cd frontend && npm run build

# Copy backend
COPY backend/ backend/

# Collect static files
RUN cd backend && python manage.py collectstatic --no-input

WORKDIR /app/backend

EXPOSE ${PORT:-8000}

CMD python manage.py migrate --no-input && gunicorn fantasy_stocks.wsgi --bind 0.0.0.0:${PORT:-8000}
