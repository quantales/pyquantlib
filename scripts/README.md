# Development Scripts

Utility scripts for common development tasks.

## Usage

Run from project root:

```bash
python scripts/clean.py      # Uninstall + remove build artifacts
python scripts/rebuild.py    # Clean + fresh install
python scripts/test.py       # Run all tests
python scripts/test.py --cov # Run with coverage
python scripts/test.py --fast # Stop on first failure
```

## Scripts

| Script | Description |
|--------|-------------|
| `clean.py` | Uninstalls pyquantlib and removes build/, dist/, *.egg-info, __pycache__ |
| `rebuild.py` | Runs clean, then `pip install -e .` |
| `test.py` | Wrapper for pytest with convenient shortcuts |
