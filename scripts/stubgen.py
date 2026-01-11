#!/usr/bin/env python
"""
Regenerate type stubs for PyQuantLib.

Usage:
    python scripts/stubgen.py          # Regenerate stubs in place
    python scripts/stubgen.py --check  # Check if stubs are up-to-date (for CI)
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def files_equal(file1: Path, file2: Path) -> bool:
    """Compare files, ignoring line ending differences."""
    try:
        text1 = file1.read_text(encoding="utf-8").replace("\r\n", "\n")
        text2 = file2.read_text(encoding="utf-8").replace("\r\n", "\n")
        return text1 == text2
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(description="Regenerate PyQuantLib type stubs")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if stubs are up-to-date (exits non-zero if outdated)",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    pkg_dir = repo_root / "pyquantlib"
    temp_dir = repo_root / ".stubgen_temp"

    # Clean temp directory
    if temp_dir.exists():
        shutil.rmtree(temp_dir)

    # Generate stubs to temp directory
    print("Generating stubs...")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pybind11_stubgen",
            "pyquantlib",
            "-o",
            str(temp_dir),
            "--ignore-all-errors",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"stubgen failed:\n{result.stderr}")
        sys.exit(1)

    temp_pkg = temp_dir / "pyquantlib"

    if args.check:
        # Compare generated stubs with committed stubs
        stub_files = [
            "__init__.pyi",
            "version.pyi",
            "_pyquantlib/__init__.pyi",
            "_pyquantlib/base.pyi",
        ]

        outdated = []
        for stub in stub_files:
            committed = pkg_dir / stub
            generated = temp_pkg / stub

            if not committed.exists():
                outdated.append(f"{stub} (missing)")
            elif not generated.exists():
                outdated.append(f"{stub} (not generated)")
            elif not files_equal(committed, generated):
                outdated.append(stub)

        # Clean up
        shutil.rmtree(temp_dir)

        if outdated:
            print("Stubs are outdated:")
            for f in outdated:
                print(f"  - {f}")
            print("\nRun 'python scripts/stubgen.py' to regenerate.")
            sys.exit(1)
        else:
            print("Stubs are up-to-date.")
            sys.exit(0)
    else:
        # Copy generated stubs to package
        stub_files = [
            ("__init__.pyi", "__init__.pyi"),
            ("version.pyi", "version.pyi"),
            ("_pyquantlib/__init__.pyi", "_pyquantlib/__init__.pyi"),
            ("_pyquantlib/base.pyi", "_pyquantlib/base.pyi"),
        ]

        # Ensure _pyquantlib directory exists
        (pkg_dir / "_pyquantlib").mkdir(exist_ok=True)

        for src, dst in stub_files:
            src_path = temp_pkg / src
            dst_path = pkg_dir / dst
            if src_path.exists():
                shutil.copy2(src_path, dst_path)
                print(f"  Updated {dst}")
            else:
                print(f"  Warning: {src} not found")

        # Clean up
        shutil.rmtree(temp_dir)
        print("Done.")


if __name__ == "__main__":
    main()
