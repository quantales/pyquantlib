# Installation

## Compatibility

| Component | Requirement |
|-----------|-------------|
| Python | 3.9, 3.10, 3.11, 3.12 |
| QuantLib | 1.40+ |
| Platforms | Windows, macOS, Linux |

PyQuantLib provides bindings for a subset of QuantLib. Foundational components are available: time handling, term structures, common instruments, and pricing engines. Coverage is actively growing. See the {doc}`api/index` for what's available.

```{note}
Check versions at runtime: `ql.__version__` (PyQuantLib) and `ql.__ql_version__` (QuantLib).
```

## Prerequisites

QuantLib must be built as a static library with `std::shared_ptr` support.

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
python -c "import pyquantlib as ql; print(f'PyQuantLib {ql.__version__} (QuantLib {ql.__ql_version__})')"
```

## Next Steps

- {doc}`quickstart` for a tutorial
- {doc}`building` for detailed build instructions
