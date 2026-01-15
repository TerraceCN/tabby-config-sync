# Stage 1: Build Frontend
FROM node:22-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy package management files
COPY frontend/package.json frontend/yarn.lock ./

# Install dependencies
RUN yarn install --frozen-lockfile

# Copy source code
COPY frontend/ ./

# Build the application
# Outputs to ../web-dist (relative to frontend/) -> /app/web-dist
RUN yarn build


# Stage 2: Build Backend Environment
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS backend-builder

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Export requirements.txt
RUN uv export --no-dev --no-hashes --no-annotate --output-file requirements.txt


# Stage 3: Final Image
FROM python:3.13-slim-bookworm

WORKDIR /app

# Copy requirements.txt from backend-builder
COPY --from=backend-builder /app/requirements.txt ./requirements.txt

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend assets from frontend-builder
COPY --from=frontend-builder /app/web-dist ./web-dist

# Copy backend application code
COPY application ./application
COPY main.py settings.py ./

# Expose the application port
EXPOSE 8000

# Run the application
CMD ["python3", "main.py"]
