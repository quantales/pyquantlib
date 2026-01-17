# Installation

## Prerequisites

- **Python 3.9+**
- **QuantLib 1.40+** built as static library with `std::shared_ptr`

```{important}
Pre-built QuantLib packages (Homebrew, vcpkg, apt) are **not compatible**. See {doc}`building` for how to build QuantLib from source.
```

## Quick Install

Once QuantLib is built and installed:

```bash
pip install git+https://github.com/quantales/pyquantlib.git
```

## Development Install

```bash
git clone https://github.com/quantales/pyquantlib.git
cd pyquantlib

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install -r requirements-dev.txt
pip install -e .
```

## Verify

```bash
python -c "import pyquantlib as ql; print(f'PyQuantLib {ql.__version__}')"
```

## Next Steps

- {doc}`quickstart` for a tutorial
- {doc}`building` for detailed build instructions
