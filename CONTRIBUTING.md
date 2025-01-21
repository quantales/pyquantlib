# Contributing to PyQuantLib

Thank you for your interest in contributing to PyQuantLib!

## Development Setup

### Prerequisites

Before you begin, ensure you have:

- **Python 3.9+**
- **CMake 3.18+**
- **C++17 compatible compiler**
  - Windows: MSVC 2019+ (Visual Studio 2019 or later)
  - macOS: Xcode 12+ or clang 10+
  - Linux: GCC 9+ or clang 10+
- **QuantLib library** (see platform-specific instructions below)
- **Boost headers** (required by QuantLib)

### Step 1: Clone the Repository

```bash
git clone https://github.com/quantales/pyquantlib.git
cd pyquantlib
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Development Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

### Step 4: Install QuantLib (Platform-Specific)

#### Windows (vcpkg - Recommended)

```powershell
# Install vcpkg if you haven't already
git clone https://github.com/microsoft/vcpkg.git
cd vcpkg
.\bootstrap-vcpkg.bat
.\vcpkg integrate install

# Install QuantLib and Boost
.\vcpkg install quantlib:x64-windows boost:x64-windows

# Set environment variable (add to your shell profile)
set VCPKG_ROOT=C:\path\to\vcpkg
```

#### macOS (Homebrew)

```bash
brew install quantlib boost cmake
```

#### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install libquantlib0-dev libboost-all-dev cmake build-essential
```

#### Fedora/RHEL

```bash
sudo dnf install quantlib-devel boost-devel cmake gcc-c++
```

### Step 5: Build and Install in Development Mode

```bash
# Build and install in editable mode
pip install -e .

# Or with verbose output for debugging:
pip install -e . -v
```

### Build Options

#### Parallel Builds

Ninja (the default build tool) auto-detects CPU cores. To override:

```bash
# Set number of parallel jobs (e.g., 8 cores)
# Windows PowerShell:
$env:CMAKE_BUILD_PARALLEL_LEVEL = 8
pip install -e .

# macOS/Linux:
CMAKE_BUILD_PARALLEL_LEVEL=8 pip install -e .
```

#### Clean Build

To force a complete rebuild:

```bash
# Windows PowerShell:
Remove-Item -Recurse -Force build, *.egg-info -ErrorAction SilentlyContinue
pip install -e .

# macOS/Linux:
rm -rf build *.egg-info
pip install -e .
```

#### Non-Editable Install

For a regular installation (copies to site-packages):

```bash
pip install .
pip install .[dev]  # with dev dependencies
```

### Step 6: Verify Installation

```bash
# Run the test suite
pytest

# Or run a quick smoke test
python -c "import pyquantlib as ql; print(f'PyQuantLib {ql.__version__} with QuantLib {ql.__ql_version__}')"
```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pyquantlib

# Run specific test file
pytest tests/test_date.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Run linter
ruff check src/ tests/

# Run type checker
mypy src/
```

### Building Wheels

```bash
# Build wheel
python -m build

# Wheels will be in dist/
```

## Project Structure

```
pyquantlib/
├── CMakeLists.txt        # CMake build configuration
├── pyproject.toml        # Python package metadata
├── requirements-dev.txt  # Development dependencies
├── include/              # C++ headers
│   └── pyquantlib/
├── src/                  # C++ source files (pybind11 bindings)
│   ├── main.cpp          # Module entry point
│   ├── core/             # Core bindings (Quote, Date, etc.)
│   ├── time/             # Time-related bindings
│   └── ...
├── pyquantlib/           # Python package
│   └── __init__.py
└── tests/                # Python test suite
```

## Adding New Bindings

See the existing bindings in `src/` for examples. The general pattern is:

1. Create a new `.cpp` file in the appropriate subdirectory
2. Declare the binding function in `include/pyquantlib/pyquantlib.h`
3. Register the binding in the module's `all.cpp` file
4. Add tests in `tests/`

## Code Style

- **C++**: Follow the existing style (clang-format configuration coming soon)
- **Python**: Use ruff for formatting and linting

## Questions?

Open an issue on GitHub or reach out to the maintainers.
