FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# System deps for psycopg, lancedb
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

# Create runtime directories
RUN mkdir -p /app/storage

EXPOSE 8000

ENV RUN_MODE=hybrid \
    PORTFOLIO_AGENT_HOST=0.0.0.0 \
    PORTFOLIO_AGENT_PORT=8000

CMD ["python", "main.py"]
