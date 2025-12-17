# Reusable GitHub Actions Workflows

Centralized Python CI/CD workflows for trading-cz projects.

## Available Workflows

### 1. `python-ci.yml`  Continuous Integration

Runs dependency checks, audits for vulnerabilities, and executes tests.

**Note:** Linting, type checking, and code formatting are handled by `megalinter.yml` workflow.

**Usage:**

```yaml
# .github/workflows/ci.yml in your repo
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ci:
    uses: trading-cz/github-action/.github/workflows/python-ci.yml@main
    with:
      python-version: ''3.12''
      test-dir: tests
```

**Inputs:**

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `python-version` | string | `3.12` | Python version (e.g., `3.12`, `3.11`) |
| `test-dir` | string | `tests` | Directory containing test files |

**Jobs:**

- **dependencies**  Checks for conflicts, validates dependency tree, audits for vulnerabilities
- **test**  Runs pytest

---

### 2. `python-build-docker.yml`  Docker Build & Push

Builds multi-arch Docker image and pushes to container registry (GHCR).  
Runs on version tags (`v*.*.*`) or manual dispatch.

**Usage:**

```yaml
# .github/workflows/build-and-push.yml in your repo
name: Build and Push Docker Image

on:
  push:
    tags:
      - ''v*.*.*''
  workflow_dispatch:
    inputs:
      version:
        description: ''Version tag (e.g., v0.0.1)''
        required: true
        type: string

jobs:
  build-and-push:
    uses: trading-cz/github-action/.github/workflows/python-build-docker.yml@main
    with:
      python-version: ''3.12''
      dockerfile-path: ''Dockerfile''
      registry: ''ghcr.io''
      image-name: ${{ github.repository }}
```

**Inputs:**

| Input | Type | Default | Required | Description |
|-------|------|---------|----------|-------------|
| `python-version` | string | `3.12` |  | Python version |
| `dockerfile-path` | string | `Dockerfile` |  | Path to Dockerfile |
| `registry` | string | `ghcr.io` |  | Container registry |
| `image-name` | string |  |  | Image name (e.g., `owner/repo`) |

**Outputs:**

| Output | Description |
|--------|-------------|
| `version` | Docker image version tag (extracted from git tag) |
| `digest` | Docker image digest |

**Jobs:**

- **test**  Runs tests before building
- **build-and-push**  Builds & pushes multi-arch image (amd64, arm64) to registry

**Features:**

- Extracts version from git tag (e.g., `v0.0.4`  `0.0.4`)
- Prevents overwriting existing versions
- Builds for `linux/amd64` and `linux/arm64`
- Uses GitHub Actions cache for faster builds
- Tags with both version and `latest`

---

### 3. `python-build-wheel.yml`  Python Wheel Build & Push

Builds Python package (wheel) and publishes to GitHub Releases.  
Runs on version tags (`v*.*.*`) or manual dispatch.

**Usage:**

```yaml
# .github/workflows/build-and-push.yml in your repo
name: Build and Push Python Package

on:
  push:
    tags:
      - ''v*.*.*''
  workflow_dispatch:
    inputs:
      version:
        description: ''Version tag (e.g., v0.0.1)''
        required: true
        type: string

jobs:
  build-and-push:
    uses: trading-cz/github-action/.github/workflows/python-build-wheel.yml@main
    with:
      python-version: ''3.12''
      pyproject-path: ''pyproject.toml''
```

**Inputs:**

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `python-version` | string | `3.12` | Python version |
| `pyproject-path` | string | `pyproject.toml` | Path to pyproject.toml |

**Outputs:**

| Output | Description |
|--------|-------------|
| `version` | Package version (extracted from git tag) |

**Jobs:**

- **verify-generated-models**  Ensures `src/tradingcz/model/kafka/` exists (model-specific check)
- **build-and-push**  Builds wheel, updates version in pyproject.toml, publishes to GitHub Releases

**Features:**

- Extracts version from git tag
- Updates version in `pyproject.toml`
- Builds package with `python -m build`
- Creates GitHub Release with wheel as artifact
- Generates release notes automatically

---

### 4. `megalinter.yml`  Comprehensive Code Quality & Linting

Validates and auto-fixes code quality issues (linting, formatting, type checking).  
Runs on all PRs and pushes to main.

**Configuration:** `.mega-linter.yml` + `.github/actionlint.yaml`

**Linters Enabled:**
- **Python:** Pylint, Black, Mypy, Ruff
- **YAML:** Prettier
- **Markdown:** MarkdownLint
- **GitHub Actions:** ActionLint

**Features:**
- Auto-fixes applicable issues
- Auto-commits fixes back to branch/PR
- Posts results in PR comments
- Uploads reports as artifacts
- Concurrency control (cancels old runs)

**Usage:**
This workflow runs automaticallyno configuration needed in calling repos.

---

## Integration Examples

### ingestion-alpaca

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ci:
    uses: trading-cz/github-action/.github/workflows/python-ci.yml@main
    with:
      python-version: ''3.12''
      test-dir: tests
```

### model

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ci:
    uses: trading-cz/github-action/.github/workflows/python-ci.yml@main
    with:
      python-version: ''3.12''
      test-dir: tests
```

---

## Reference Versions

Always pin to a specific ref:

```yaml
uses: trading-cz/github-action/.github/workflows/python-ci.yml@main
```

- `@main`  Latest version
- `@v1.0.0`  Specific release tag
