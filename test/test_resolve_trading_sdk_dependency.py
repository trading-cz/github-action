"""Unit tests for the MegaLinter trading-sdk dependency resolver."""

from __future__ import annotations

import importlib.util
import os
import unittest
from contextlib import chdir
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch


SCRIPT_PATH = (
    Path(__file__).parents[1]
    / ".github"
    / "script"
    / "resolve-trading-sdk-dependency-for-megalinter.py"
)
MODULE_SPEC = importlib.util.spec_from_file_location("sdk_dependency_resolver", SCRIPT_PATH)
if MODULE_SPEC is None or MODULE_SPEC.loader is None:
    raise RuntimeError(f"Unable to load {SCRIPT_PATH}")
RESOLVER = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(RESOLVER)


class ResolveTradingSdkDependencyTests(unittest.TestCase):
    """Verify the resolver output used by the reusable workflow."""

    def test_main_writes_declared_dependency_to_github_output(self) -> None:
        """The project declaration is copied to the step output unchanged."""
        with TemporaryDirectory() as temporary_directory:
            project_directory = Path(temporary_directory)
            output_path = project_directory / "github-output"
            (project_directory / "pyproject.toml").write_text(
                '[project]\ndependencies = [\n'
                '    "trading-sdk @ git+https://github.com/trading-cz/sdk@v0.1.25",\n'
                ']\n',
                encoding="utf-8",
            )

            with chdir(project_directory), patch.dict(os.environ, {"GITHUB_OUTPUT": str(output_path)}):
                result = RESOLVER.main()

            self.assertEqual(result, 0)
            self.assertEqual(
                output_path.read_text(encoding="utf-8"),
                "dependency=trading-sdk @ git+https://github.com/trading-cz/sdk@v0.1.25\n",
            )

    def test_main_writes_empty_output_without_sdk_dependency(self) -> None:
        """Projects without trading-sdk produce an empty step output."""
        with TemporaryDirectory() as temporary_directory:
            project_directory = Path(temporary_directory)
            output_path = project_directory / "github-output"
            (project_directory / "pyproject.toml").write_text(
                '[project]\ndependencies = ["pydantic>=2.0"]\n',
                encoding="utf-8",
            )

            with chdir(project_directory), patch.dict(os.environ, {"GITHUB_OUTPUT": str(output_path)}):
                result = RESOLVER.main()

            self.assertEqual(result, 0)
            self.assertEqual(output_path.read_text(encoding="utf-8"), "dependency=\n")


if __name__ == "__main__":
    unittest.main()