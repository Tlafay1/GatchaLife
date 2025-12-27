# Stage 1: Base
FROM python:3.12-slim AS base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Stage 2: Builder (for production wheels)
FROM base AS builder

RUN apt-get update && apt-get install -y --no-install-recommends gcc

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 3: Development
FROM base AS dev

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && gunicorn gatchalife.wsgi:application --bind 0.0.0.0:8000 --workers 2 --threads 4 --reload"]

# Stage 4: Production
FROM base AS prod

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/*

COPY . .

# Create directory for static files
RUN mkdir -p /app/staticfiles && mkdir -p /app/static/images

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn gatchalife.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 4 --timeout 120"]
