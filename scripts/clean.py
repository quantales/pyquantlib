#!/usr/bin/env python
"""Clean build artifacts and uninstall pyquantlib."""

import shutil
import subprocess
import sys
from pathlib import Path


def main():
    root = Path(__file__).parent.parent

    # Uninstall package
    print("Uninstalling pyquantlib...")
    subprocess.run(
        [sys.executable, "-m", "pip", "uninstall", "pyquantlib", "-y"],
        capture_output=True,
    )

    # Directories to remove
    dirs_to_clean = [
        root / "build",
        root / "dist",
        root / ".eggs",
        root / "pyquantlib.egg-info",
    ]

    # Also find any __pycache__ and .egg-info dirs
    dirs_to_clean.extend(root.rglob("__pycache__"))
    dirs_to_clean.extend(root.rglob("*.egg-info"))

    removed = []
    for d in dirs_to_clean:
        if d.exists() and d.is_dir():
            shutil.rmtree(d)
            removed.append(d.relative_to(root))

    if removed:
        print(f"Removed: {', '.join(str(d) for d in removed)}")
    else:
        print("Nothing to clean.")

    print("Done.")


if __name__ == "__main__":
    main()
