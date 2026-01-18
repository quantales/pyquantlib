#!/usr/bin/env python
"""
Build PyQuantLib documentation.

Usage:
    python scripts/build_docs.py          # Build docs
    python scripts/build_docs.py --open   # Build and open in browser
    python scripts/build_docs.py --clean  # Clean cache and build
"""

import argparse
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Build PyQuantLib documentation")
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open docs in browser after building",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean Sphinx cache before building",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    docs_dir = repo_root / "docs"
    build_dir = docs_dir / "_build"
    html_dir = build_dir / "html"

    # Clean cache
    if args.clean and build_dir.exists():
        print("Cleaning Sphinx cache...")
        shutil.rmtree(build_dir)

    # Build docs
    print("Building documentation...")
    result = subprocess.run(
        ["sphinx-build", "-b", "html", ".", "_build/html"],
        cwd=docs_dir,
    )

    if result.returncode != 0:
        print("Documentation build failed.")
        sys.exit(1)

    print(f"Documentation built: {html_dir}")

    # Open in browser
    if args.open:
        index = html_dir / "index.html"
        if index.exists():
            webbrowser.open(index.as_uri())
        else:
            print(f"Warning: {index} not found")


if __name__ == "__main__":
    main()
