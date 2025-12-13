#!/usr/bin/env python
"""Run test suite with common options."""

import subprocess
import sys
from pathlib import Path


def main():
    root = Path(__file__).parent.parent

    args = sys.argv[1:]
    
    # Default: run pytest with verbose output
    cmd = [sys.executable, "-m", "pytest"]
    
    if not args:
        # No args: run all tests
        cmd.append("-v")
    elif args == ["--cov"]:
        # Coverage mode
        cmd.extend(["--cov=pyquantlib", "--cov-report=term-missing"])
    elif args == ["--fast"]:
        # Quick smoke test: stop on first failure
        cmd.extend(["-x", "-v"])
    else:
        # Pass through any other args
        cmd.extend(args)

    print(f"Running: {' '.join(cmd)}")
    print()
    
    result = subprocess.run(cmd, cwd=root)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
