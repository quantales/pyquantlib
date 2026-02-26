# Installation

## Compatibility

- **Python**: 3.10, 3.11, 3.12, 3.13
- **QuantLib**: 1.40+
- **Platforms**: Windows, macOS, Linux

PyQuantLib provides bindings for a subset of QuantLib. Foundational components are available: time handling, term structures, common instruments, and pricing engines. Coverage is actively growing. See the {doc}`api/index` for what's available.

```{note}
Check versions at runtime: `ql.__version__` (PyQuantLib) and `ql.QL_VERSION` (QuantLib).
```

## Install from PyPI

```bash
pip install pyquantlib
```

Pre-built wheels are available for Python 3.10--3.13 on Linux (x86_64), macOS (ARM), and Windows (x64). QuantLib is statically linked -- no separate installation required.

## Install from Source

To install the latest development version from GitHub, QuantLib must first be built as a static library with `std::shared_ptr` support. See {doc}`building` for detailed build instructions.

```{important}
Pre-built QuantLib packages (Homebrew, vcpkg, apt) are **not compatible**. QuantLib must be built from source.
```

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
python -c "import pyquantlib as ql; print(f'PyQuantLib {ql.__version__} (QuantLib {ql.QL_VERSION})')"
```

## Next Steps

- {doc}`quickstart` for a tutorial
- {doc}`building` for detailed build instructions
