FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt

RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY src/ .

COPY docker/scripts/wait_for_db.py /wait_for_db.py
COPY docker/scripts/entrypoint.sh /entrypoint.sh

RUN pip install --no-cache-dir psycopg2-binary

RUN chmod +x /wait_for_db.py /entrypoint.sh

ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
