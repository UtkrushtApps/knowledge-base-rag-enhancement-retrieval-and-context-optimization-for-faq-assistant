#!/bin/bash
set -e

if (! docker stats --no-stream ); then
    echo "[ERROR] Docker must be running!" >&2
    exit 1
fi

if docker ps -a --format '{{.Names}}' | grep -Eq '^faq-chroma$'; then
    echo "[INFO] Removing old faq-chroma container..."
    docker-compose down -v
fi

echo "[INFO] Starting Chroma vector DB container..."
docker-compose up -d --build
sleep 3
echo "[INFO] Initializing directories and dependencies..."
docker-compose exec faq-chroma python scripts/init_container.py

echo "[INFO] Populating FAQ database..."
docker-compose exec faq-chroma python scripts/process_documents.py

echo "[INFO] Verifying Chroma setup..."
docker-compose exec faq-chroma python scripts/verify_setup.py

echo "[SUCCESS] FAQ retrieval environment ready.\n"
