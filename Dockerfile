# syntax=docker/dockerfile:1
FROM python:3.13-alpine AS builder

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.13-alpine

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app

COPY imdb_server.py .
COPY entrypoint.sh /usr/local/bin/imdb-mcp-server

RUN chmod +x /usr/local/bin/imdb-mcp-server

ENV PATH="/opt/venv/bin:$PATH"

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

ENTRYPOINT ["imdb-mcp-server"]

LABEL maintainer="Uzay Sozen" \
      version="1.0" \
      description="IMDB MCP Server"