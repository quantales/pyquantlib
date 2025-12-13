#!/usr/bin/env python
"""Clean and rebuild pyquantlib from scratch."""

import subprocess
import sys
from pathlib import Path


def main():
    root = Path(__file__).parent.parent
    scripts_dir = Path(__file__).parent

    # Run clean
    print("=" * 50)
    print("CLEAN")
    print("=" * 50)
    subprocess.run([sys.executable, scripts_dir / "clean.py"], check=True)

    # Install in editable mode
    print()
    print("=" * 50)
    print("BUILD & INSTALL")
    print("=" * 50)
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-e", "."],
        cwd=root,
    )

    if result.returncode == 0:
        print()
        print("=" * 50)
        print("SUCCESS")
        print("=" * 50)
        # Show version
        subprocess.run([
            sys.executable, "-c",
            "import pyquantlib as ql; print(f'PyQuantLib {ql.__version__} with QuantLib {ql.__ql_version__}')"
        ])
    else:
        print()
        print("=" * 50)
        print("BUILD FAILED")
        print("=" * 50)
        sys.exit(1)


if __name__ == "__main__":
    main()
