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
- **Boost headers** (required by QuantLib)
- **QuantLib 1.40+** built with required configuration (see below)

### QuantLib Build Requirements

> ⚠️ **Critical**: PyQuantLib requires QuantLib built with `std::shared_ptr`.

PyQuantLib uses pybind11, which defaults to `std::shared_ptr` as its holder type. QuantLib must be compiled with matching settings to avoid runtime errors and segmentation faults.

**Required CMake flags:**

| Flag | Value | Notes |
|------|-------|-------|
| `QL_USE_STD_SHARED_PTR` | `ON` | **Required** - must be explicitly set |
| `QL_USE_STD_OPTIONAL` | `ON` | Default as of QuantLib 1.40 |
| `QL_USE_STD_ANY` | `ON` | Default as of QuantLib 1.40 |

**Pre-built packages won't work**: Homebrew, vcpkg, and apt packages use default settings (`boost::shared_ptr`) and are incompatible with PyQuantLib.

---

## Building QuantLib from Source

### Download QuantLib 1.40

```bash
# Download release
wget https://github.com/lballabio/QuantLib/releases/download/v1.40/QuantLib-1.40.tar.gz
tar xzf QuantLib-1.40.tar.gz
cd QuantLib-1.40

# Or clone the repo
git clone https://github.com/lballabio/QuantLib.git
cd QuantLib
git checkout v1.40
```

### Windows

**Prerequisites:**
- Visual Studio 2019 or later
- Boost (headers only, or full install)

```powershell
# Install Boost via vcpkg (headers are sufficient)
vcpkg install boost:x64-windows

# Configure QuantLib (QL_USE_STD_OPTIONAL and QL_USE_STD_ANY are ON by default as of QuantLib 1.40)
mkdir build
cd build
cmake .. -G "Visual Studio 16 2019" -A x64 ^
    -DQL_USE_STD_SHARED_PTR=ON ^
    -DCMAKE_BUILD_TYPE=Release ^
    -DCMAKE_INSTALL_PREFIX=C:/QuantLib ^
    -DBoost_ROOT=C:/vcpkg/installed/x64-windows

# Build and install
cmake --build . --config Release --parallel 8
cmake --install . --config Release

# Set environment variable for PyQuantLib to find it
set QL_DIR=C:\QuantLib
```

### macOS

**Prerequisites:**
```bash
# Install Boost (headers are sufficient)
brew install boost cmake
```

**Build QuantLib:**
```bash
# QL_USE_STD_OPTIONAL and QL_USE_STD_ANY are ON by default as of QuantLib 1.40
mkdir build && cd build
cmake .. \
    -DQL_USE_STD_SHARED_PTR=ON \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr/local

make -j$(sysctl -n hw.ncpu)
sudo make install
```

### Linux (Ubuntu/Debian)

**Prerequisites:**
```bash
sudo apt-get update
sudo apt-get install libboost-all-dev cmake build-essential
```

**Build QuantLib:**
```bash
# QL_USE_STD_OPTIONAL and QL_USE_STD_ANY are ON by default as of QuantLib 1.40
mkdir build && cd build
cmake .. \
    -DQL_USE_STD_SHARED_PTR=ON \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr/local

make -j$(nproc)
sudo make install
sudo ldconfig
```

### Verify QuantLib Configuration

After installation, verify the flags are set correctly:

```bash
# Check config.hpp
grep -E "QL_USE_STD_(SHARED_PTR|OPTIONAL|ANY)" /usr/local/include/ql/config.hpp
```

Expected output:
```cpp
#define QL_USE_STD_ANY
#define QL_USE_STD_OPTIONAL
#define QL_USE_STD_SHARED_PTR
```

---

## PyQuantLib Development Setup

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

### Step 4: Build and Install in Development Mode

```bash
# Build and install in editable mode
pip install -e .

# Or with verbose output for debugging:
pip install -e . -v
```

### Step 5: Verify Installation

```bash
# Run the test suite
pytest

# Or run a quick smoke test
python -c "import pyquantlib as ql; print(f'PyQuantLib {ql.__version__} with QuantLib {ql.__ql_version__}')"
```

---

## Build Options

### Parallel Builds

Ninja (the default build tool) auto-detects CPU cores. To override:

```bash
# Set number of parallel jobs (e.g., 8 cores)
# Windows PowerShell:
$env:CMAKE_BUILD_PARALLEL_LEVEL = 8
pip install -e .

# macOS/Linux:
CMAKE_BUILD_PARALLEL_LEVEL=8 pip install -e .
```

### Clean Build

To force a complete rebuild:

```bash
# Windows PowerShell:
Remove-Item -Recurse -Force build, *.egg-info -ErrorAction SilentlyContinue
pip install -e .

# macOS/Linux:
rm -rf build *.egg-info
pip install -e .
```

### Non-Editable Install

For a regular installation (copies to site-packages):

```bash
pip install .
pip install .[dev]  # with dev dependencies
```

---

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

---

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

---

## Adding New Bindings

See the existing bindings in `src/` for examples. The general pattern is:

1. Create a new `.cpp` file in the appropriate subdirectory
2. Declare the binding function in `include/pyquantlib/pyquantlib.h`
3. Register the binding in the module's `all.cpp` file
4. Add tests in `tests/`

---

## Code Style

- **C++**: Follow the existing style (clang-format configuration coming soon)
- **Python**: Use ruff for formatting and linting

---

## Troubleshooting

### "undefined symbol" or segmentation fault at import

This usually means QuantLib was built with `boost::shared_ptr` (the default) instead of `std::shared_ptr`. Rebuild QuantLib with `QL_USE_STD_SHARED_PTR=ON`.

### CMake can't find QuantLib

Set the `QL_DIR` environment variable to your QuantLib installation prefix:

```bash
# Windows
set QL_DIR=C:\QuantLib

# macOS/Linux
export QL_DIR=/usr/local
```

### Boost not found

Ensure Boost is installed and discoverable. You can hint CMake:

```bash
cmake -DBoost_ROOT=/path/to/boost ...
```

---

## Questions?

Open an issue on GitHub or reach out to the maintainers.
