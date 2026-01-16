#!/usr/bin/env python
"""
Build PyQuantLib documentation.

Usage:
    python scripts/build_docs.py          # Build docs
    python scripts/build_docs.py --open   # Build and open in browser
"""

import argparse
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
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    docs_dir = repo_root / "docs"
    build_dir = docs_dir / "_build" / "html"

    # Build docs
    print("Building documentation...")
    result = subprocess.run(
        ["sphinx-build", "-b", "html", ".", "_build/html"],
        cwd=docs_dir,
    )

    if result.returncode != 0:
        print("Documentation build failed.")
        sys.exit(1)

    print(f"Documentation built: {build_dir}")

    # Open in browser
    if args.open:
        index = build_dir / "index.html"
        if index.exists():
            webbrowser.open(index.as_uri())
        else:
            print(f"Warning: {index} not found")


if __name__ == "__main__":
    main()
