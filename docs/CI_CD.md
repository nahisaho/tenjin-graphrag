# CI/CD Configuration

This project uses GitHub Actions for continuous integration and deployment.

## Workflows

### CI (`ci.yml`)
Main continuous integration pipeline that runs on every push and pull request.

**Jobs:**
- **Lint & Format**: Runs ruff linter and formatter checks
- **Test**: Runs unit and integration tests with Neo4j service
- **Coverage**: Generates test coverage report (minimum 90%)
- **Security**: Runs safety and bandit security scans
- **Build**: Builds the Python package

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

### E2E Tests (`e2e.yml`)
End-to-end tests that require full infrastructure.

**Jobs:**
- **E2E Tests**: Seeds test data and runs full E2E test suite

**Triggers:**
- Push to `main` branch
- Daily schedule (2:00 AM UTC)
- Manual dispatch

### Docker Build (`docker.yml`)
Tests Docker image builds and docker-compose setup.

**Jobs:**
- **Build Docker Image**: Builds and tests the production image
- **Test Docker Compose**: Tests the full docker-compose stack

**Triggers:**
- Push/PR with changes to Docker-related files or source code

### Release (`release.yml`)
Creates releases and publishes Docker images.

**Jobs:**
- **Create Release**: Builds package and creates GitHub release
- **Build & Push Docker**: Builds and pushes Docker images to GHCR

**Triggers:**
- Git tags starting with `v` (e.g., `v0.1.0`, `v1.0.0-beta`)

### Dependency Review (`dependency-review.yml`)
Reviews dependencies for security vulnerabilities and license compliance.

**Jobs:**
- **Dependency Review**: Checks for high severity vulnerabilities and restricted licenses

**Triggers:**
- Pull requests to `main` branch

## Environment Variables

### Required for Tests
```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=testpassword
CHROMADB_PATH=./data/chromadb
EMBEDDING_PROVIDER=local
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### Required for Release
- `GITHUB_TOKEN`: Automatically provided by GitHub Actions
- `CODECOV_TOKEN` (optional): For Codecov coverage uploads

## Local Development

### Running CI Checks Locally

```bash
# Lint
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/

# Tests
uv run pytest tests/unit/ tests/integration/ -v

# Coverage
uv run pytest tests/ --cov=src/tengin_mcp --cov-report=term-missing

# Security
uv pip install safety bandit
uv run safety check
uv run bandit -r src/ -ll -ii

# Build
uv build
```

### Running E2E Tests Locally

```bash
# Start infrastructure
docker compose up -d neo4j chromadb

# Wait for Neo4j
sleep 30

# Seed data
uv run python -m tengin_mcp.scripts.seed_data

# Run E2E tests
uv run pytest tests/e2e/ -v
```

## Creating a Release

1. Update version in `pyproject.toml`
2. Commit changes: `git commit -m "Bump version to x.y.z"`
3. Create and push tag: `git tag -a vx.y.z -m "Release x.y.z" && git push origin vx.y.z`

The release workflow will automatically:
- Run tests
- Build the package
- Create a GitHub release with changelog
- Build and push Docker images to GHCR

## Docker Images

Images are published to GitHub Container Registry (GHCR):

```bash
# Pull latest stable
docker pull ghcr.io/nahisaho/tengin-graphrag:latest

# Pull specific version
docker pull ghcr.io/nahisaho/tengin-graphrag:0.1.0
```

## Badges

Add these badges to your README:

```markdown
![CI](https://github.com/nahisaho/TENGIN-GraphRAG/actions/workflows/ci.yml/badge.svg)
![E2E](https://github.com/nahisaho/TENGIN-GraphRAG/actions/workflows/e2e.yml/badge.svg)
[![codecov](https://codecov.io/gh/nahisaho/TENGIN-GraphRAG/branch/main/graph/badge.svg)](https://codecov.io/gh/nahisaho/TENGIN-GraphRAG)
```
