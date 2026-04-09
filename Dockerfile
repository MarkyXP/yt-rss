# Use UV python for the base image
FROM python:3.12-slim
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install curl and clean up apt cache to keep the image slim
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Run uv to build the application dependencies
WORKDIR /app
COPY . .
RUN uv sync --frozen
# Run
CMD ["uv", "run", "python", "main.py"]
