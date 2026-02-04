# Development Scripts

Utility scripts for common development tasks.

## Usage

Run from project root:

```bash
python scripts/clean.py       # Uninstall + remove build artifacts
python scripts/rebuild.py     # Clean + fresh install
python scripts/test.py        # Run all tests
python scripts/test.py --cov  # Run with coverage
python scripts/test.py --fast # Stop on first failure
python scripts/stubgen.py     # Regenerate type stubs
python scripts/build_docs.py         # Build Sphinx documentation
python scripts/build_docs.py --open  # Build and open in browser
python scripts/build_docs.py --clean # Clean cache and rebuild
```

## Scripts

| Script | Description |
|--------|-------------|
| `clean.py` | Uninstalls pyquantlib and removes build/, dist/, *.egg-info, __pycache__ |
| `rebuild.py` | Runs clean, then `pip install -e .` |
| `test.py` | Wrapper for pytest with convenient shortcuts |
| `stubgen.py` | Regenerates .pyi type stub files for IDE support |
| `build_docs.py` | Builds Sphinx documentation |
