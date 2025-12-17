# github-actions

Centralized, reusable GitHub Actions workflows for trading-cz Python projects.

## Overview

This repository provides parameterized, reusable GitHub Actions workflows via `workflow_call`:

- **`megalinter.yml`** — Code quality & linting (auto-fixes enabled)
- **`python-ci.yml`** — Continuous Integration (lint, test, type-check)
- **`python-build-docker.yml`** — Docker image build & push to GHCR
- **`python-build-wheel.yml`** — Python wheel build & publish to GitHub Releases

Instead of duplicating CI logic across repos, teams can call these workflows from their own `.github/workflows/` directories.

## Quick Start

### Add MegaLinter workflow to your repo

Create `.github/workflows/megalinter.yml` in your repository:

```yaml
name: MegaLinter

on:
  pull_request:
    branches: [main]

jobs:
  megalinter:
    uses: trading-cz/github-action/.github/workflows/megalinter.yml@main
```

The workflow will:
- Use your repo's `.mega-linter.yml` if it exists
- Fallback to defaults from github-action (optimized linter set: ruff, black, isort, mypy)
- Auto-fix issues on PRs/push events
- Report results in PR comments and job summaries

**Optional:** Create `.mega-linter.yml` in your repo to customize which linters run.

### Add CI workflow to your repo

Create `.github/workflows/ci.yml` in your repository:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ci:
    uses: trading-cz/github-actions/.github/workflows/python-ci.yml@main
    with:
      python-version: '3.12'
      source-dir: tradingcz
      test-dir: tests
```

### Add Docker build workflow to your repo

Create `.github/workflows/build-and-push.yml`:

```yaml
name: Build and Push Docker Image

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  build:
    uses: trading-cz/github-actions/.github/workflows/python-build-docker.yml@main
    with:
      image-name: ${{ github.repository }}
```

### Add Wheel build workflow to your repo

Create `.github/workflows/build-and-push.yml`:

```yaml
name: Build and Push Python Package

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  build:
    uses: trading-cz/github-actions/.github/workflows/python-build-wheel.yml@main
```

## Repository Structure

```
github-action/
├── .github/workflows/
│   ├── megalinter.yml             # Reusable code quality workflow
│   ├── python-ci.yml              # Reusable CI workflow
│   ├── python-build-docker.yml    # Reusable Docker workflow
│   ├── python-build-wheel.yml     # Reusable wheel workflow
│   └── README.md                  # Detailed workflow documentation
├── .mega-linter.yml               # Default MegaLinter configuration
└── README.md                      # This file
```

## Workflows Documentation

See [`.github/workflows/README.md`](.github/workflows/README.md) for:
- Detailed input/output specifications
- Full usage examples
- Integration patterns

## Which Workflow to Use?

| Use Case | Workflow | Triggered On |
|----------|----------|-------------|
| Lint, format, security scan | `megalinter.yml` | Every PR to main |
| Run tests, lint, type-check | `python-ci.yml` | Every push/PR to main |
| Build & push Docker image | `python-build-docker.yml` | Version tag (v*.*.*) |
| Build & publish Python wheel | `python-build-wheel.yml` | Version tag (v*.*.*) |

## Integration Examples

See repos for real-world usage:

- **ingestion-alpaca** — Uses `python-ci.yml` + `python-build-docker.yml`
- **model** — Uses `python-ci.yml` + `python-build-wheel.yml`

## Contributing

When updating workflows:

1. Test locally with `act` (optional)
2. Update corresponding inputs/outputs in [`.github/workflows/README.md`](.github/workflows/README.md)
3. Tag releases: `git tag -a v1.0.0 -m "Release v1.0.0"` (optional, for breaking changes)
4. Push: `git push origin main --follow-tags`

## Version Pinning

Always reference workflows with a specific ref:

```yaml
uses: trading-cz/github-actions/.github/workflows/python-ci.yml@main
```

Recommended approach:
- `@main` for quick fixes
- `@v1.0.0` for stable releases (pin in critical repos)
