# TENGIN-GraphRAG Dockerfile
# Multi-stage build for optimized production image

# ==============================================================================
# Stage 1: Build stage
# ==============================================================================
FROM python:3.12-slim AS builder

WORKDIR /app

# Install uv for fast dependency resolution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files and README (required by pyproject.toml)
COPY pyproject.toml uv.lock README.md ./

# Create virtual environment and install dependencies
RUN uv sync --frozen --no-dev --no-install-project

# Copy source code
COPY src/ ./src/
COPY data/ ./data/

# Install the project
RUN uv sync --frozen --no-dev

# ==============================================================================
# Stage 2: Production stage
# ==============================================================================
FROM python:3.12-slim AS production

WORKDIR /app

# Create non-root user for security
RUN groupadd --gid 1000 tengin && \
    useradd --uid 1000 --gid tengin --shell /bin/bash --create-home tengin

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY --from=builder /app/src /app/src
COPY --from=builder /app/data /app/data

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create directories for data with proper permissions
RUN mkdir -p /app/data/chromadb /app/data/theories && \
    chown -R tengin:tengin /app

# Switch to non-root user
USER tengin

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from tengin_mcp import __version__; print(__version__)" || exit 1

# Expose MCP server port (if using HTTP transport)
EXPOSE 8000

# Default command
CMD ["python", "-m", "tengin_mcp.server"]

# ==============================================================================
# Stage 3: Development stage
# ==============================================================================
FROM python:3.12-slim AS development

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install development tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install all dependencies including dev
RUN uv sync --frozen

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"
ENV PYTHONUNBUFFERED=1

# Default command for development
CMD ["bash"]
