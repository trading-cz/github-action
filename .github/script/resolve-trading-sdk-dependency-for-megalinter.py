#!/usr/bin/env python3
"""Resolve the checked-out project's trading-sdk requirement for MegaLinter."""

from __future__ import annotations

import os
import re
import sys
import tomllib
from pathlib import Path


SDK_DEPENDENCY_PATTERN = re.compile(
    r"^trading[-_]sdk(?:\[[^]]+\])?(?:\s|[<>=!~@])",
    re.IGNORECASE,
)


def _dependency_list(value: object) -> list[str]:
    """Return string dependencies from a TOML dependency list."""
    if not isinstance(value, list):
        return []
    return [dependency.strip() for dependency in value if isinstance(dependency, str)]


def _find_sdk_dependency(document: dict[str, object]) -> str:
    """Find the single trading-sdk requirement in a pyproject document."""
    project = document.get("project", {})
    if not isinstance(project, dict):
        return ""

    dependencies = _dependency_list(project.get("dependencies"))
    optional_dependencies = project.get("optional-dependencies", {})
    if isinstance(optional_dependencies, dict):
        for values in optional_dependencies.values():
            dependencies.extend(_dependency_list(values))

    matches = [dependency for dependency in dependencies if SDK_DEPENDENCY_PATTERN.match(dependency)]
    if len(matches) > 1:
        raise ValueError(f"Multiple trading-sdk dependencies found: {matches}")
    return matches[0] if matches else ""


def _write_output(dependency: str) -> None:
    """Write the resolved dependency to the GitHub Actions step output."""
    output_path = os.environ.get("GITHUB_OUTPUT")
    if output_path:
        with Path(output_path).open("a", encoding="utf-8") as output_file:
            output_file.write(f"dependency={dependency}\n")
    else:
        print(f"dependency={dependency}")


def main() -> int:
    """Resolve and publish the trading-sdk requirement."""
    project_path = Path("pyproject.toml")
    if not project_path.is_file():
        _write_output("")
        print("No pyproject.toml found; no trading-sdk dependency resolved.")
        return 0

    try:
        document = tomllib.loads(project_path.read_text(encoding="utf-8"))
        dependency = _find_sdk_dependency(document)
    except (OSError, tomllib.TOMLDecodeError, ValueError) as error:
        print(f"Unable to resolve trading-sdk dependency: {error}", file=sys.stderr)
        return 1

    _write_output(dependency)
    if dependency:
        print(f"Resolved trading-sdk dependency: {dependency}")
    else:
        print("No trading-sdk dependency declared.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())