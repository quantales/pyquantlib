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

> **Critical**: PyQuantLib requires QuantLib built as a **static library** with `std::shared_ptr`.

PyQuantLib uses pybind11, which defaults to `std::shared_ptr` as its holder type. Additionally, QuantLib must be built as a static library on Linux and macOS to prevent Settings singleton issues.

**Required CMake flags:**

| Flag | Value | Notes |
|------|-------|-------|
| `BUILD_SHARED_LIBS` | `OFF` | **Required on Linux/macOS** - static build prevents singleton issues |
| `CMAKE_POSITION_INDEPENDENT_CODE` | `ON` | **Required** - needed for static libs in Python modules |
| `QL_USE_STD_SHARED_PTR` | `ON` | **Required** - must be explicitly set |
| `CMAKE_MSVC_RUNTIME_LIBRARY` | `MultiThreadedDLL` | **Required on Windows** - Python extensions use dynamic runtime (`/MD`) |
| `QL_USE_STD_OPTIONAL` | `ON` | Default as of QuantLib 1.40 |
| `QL_USE_STD_ANY` | `ON` | Default as of QuantLib 1.40 |

**Why static builds?** QuantLib's `Settings` singleton uses a static local variable. When QuantLib is a shared library, Python loads modules with `RTLD_LOCAL`, which can cause the singleton to exist in multiple instances. Static linking embeds QuantLib into the Python module, ensuring a single singleton instance.

**Windows runtime library**: On Windows, `CMAKE_MSVC_RUNTIME_LIBRARY=MultiThreadedDLL` ensures QuantLib uses the dynamic C/C++ runtime (`/MD`). Python extensions require the dynamic runtime, so QuantLib must match to avoid linker errors. This setting is independent from `BUILD_SHARED_LIBS` — a static library (`.lib`) can use dynamic runtime linkage.

**Pre-built packages won't work**: Homebrew, vcpkg, and apt packages use shared builds and default settings (`boost::shared_ptr`) — they are incompatible with PyQuantLib.

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

# Configure QuantLib (static build with std::shared_ptr)
mkdir build
cd build
cmake .. -G "Visual Studio 16 2019" -A x64 ^
    -DBUILD_SHARED_LIBS=OFF ^
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON ^
    -DQL_USE_STD_SHARED_PTR=ON ^
    -DCMAKE_MSVC_RUNTIME_LIBRARY=MultiThreadedDLL ^
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
# Static build with std::shared_ptr (do NOT use Homebrew QuantLib)
mkdir build && cd build
cmake .. \
    -DBUILD_SHARED_LIBS=OFF \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
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
# Static build with std::shared_ptr
mkdir build && cd build
cmake .. \
    -DBUILD_SHARED_LIBS=OFF \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
    -DQL_USE_STD_SHARED_PTR=ON \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr/local

make -j$(nproc)
sudo make install
sudo ldconfig
```

### Verify QuantLib Configuration

After installation, verify the build configuration:

```bash
# Check config.hpp for required flags
grep -E "QL_USE_STD_(SHARED_PTR|OPTIONAL|ANY)" /usr/local/include/ql/config.hpp

# Check that it's a static library (should show .a files, not .so/.dylib)
ls -la /usr/local/lib/libQuantLib*
```

Expected config.hpp output:
```cpp
#define QL_USE_STD_ANY
#define QL_USE_STD_OPTIONAL
#define QL_USE_STD_SHARED_PTR
```

Expected library files:
```
libQuantLib.a          # Static library (correct)
# NOT libQuantLib.so or libQuantLib.dylib (shared - incorrect)
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
python -c "import pyquantlib as ql; print(f'PyQuantLib {ql.__version__} with QuantLib {ql.QL_VERSION}')"
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

### Linting

```bash
ruff check tests/ pyquantlib/
```

### Building Documentation

```bash
# Install docs dependencies (first time only)
pip install -e ".[docs]"

# Build HTML docs
cd docs
sphinx-build -b html . _build/html

# View locally
# Windows:
start _build/html/index.html
# macOS:
open _build/html/index.html
# Linux:
xdg-open _build/html/index.html
```

Or use the convenience script:

```bash
python scripts/build_docs.py
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

### File Mapping Convention

PyQuantLib mirrors QuantLib's directory structure. Each QuantLib header should have a corresponding binding file:

| QuantLib Header | PyQuantLib Binding |
|-----------------|-------------------|
| `ql/pricingengines/vanilla/mcamericanengine.hpp` | `src/pricingengines/vanilla/mcamericanengine.cpp` |
| `ql/termstructures/yield/flatforward.hpp` | `src/termstructures/yield/flatforward.cpp` |
| `ql/time/date.hpp` | `src/time/date.cpp` |
| `ql/instrument.hpp` | `src/core/instrument.cpp` |

Top-level QuantLib files (e.g., `ql/instrument.hpp`) go to `src/core/`.

### Steps to Add a Binding

1. Create a new `.cpp` file in the appropriate subdirectory (matching QuantLib's structure)
2. Declare the binding function in `include/pyquantlib/pyquantlib.h`
3. Register the binding in the module's `all.cpp` file
4. Add tests in `tests/`

See the existing bindings in `src/` for examples.

---

## Type Stubs

PyQuantLib includes `.pyi` stub files for IDE support (autocomplete, type hints). These are generated using `pybind11-stubgen`.

**For contributors:** Do not regenerate stubs in PRs. The maintainer will regenerate them after merging binding changes.

**For maintainers:** After changing bindings, regenerate stubs:

```bash
# Regenerate all stubs
python scripts/stubgen.py

# Check if stubs are up-to-date (local only)
python scripts/stubgen.py --check
```

> **Note:** `pybind11-stubgen` generates imports in non-deterministic order, so stubs generated on Windows may differ from Linux/macOS even with identical bindings. For this reason, CI does not validate stubs. Regenerate on the same platform where stubs were originally generated.

**Tips for good stubs:**

| Binding practice | Stub result |
|------------------|-------------|
| `py::arg("paramName")` | Named parameters in hints |
| Docstrings on classes/methods | Docstrings in stubs |
| `py::overload_cast<...>` | `@typing.overload` signatures |

**Manual generation (if needed):**

```bash
# Install (included in dev dependencies)
pip install pybind11-stubgen

# Generate to custom location
pybind11-stubgen pyquantlib -o stubs --ignore-all-errors
```

---

## Common Binding Pitfalls

### Bridge-Pattern Classes (DayCounter, Calendar, etc.)

QuantLib uses the bridge pattern for classes like `DayCounter` and `Calendar`. The base class constructor creates an empty/invalid object with no implementation, which causes import failures when used as a default argument.

**Convention**: Use `Actual365Fixed()` as the default for `DayCounter` parameters:

```cpp
// Good: concrete default (our convention)
py::arg("dayCounter") = Actual365Fixed()

// Good: required argument (no default)
py::arg("dayCounter")

// Bad: causes "no day counter implementation provided" at import
py::arg("dayCounter") = DayCounter()
```

**Why Actual365Fixed?**
- Already used throughout the codebase (e.g., `TermStructure`, `YieldTermStructure`)
- Common industry convention
- Simple, predictable behavior

**Note**: `SimpleDayCounter` is NOT suitable as a default — it only works correctly with `NullCalendar`.

### Enum Pass-by-Reference

pybind11 enum values are singletons. Never pass by reference and modify:

```cpp
// Bad: corrupts enum singleton
.def("check", [](const Foo& self, SomeEnum::Type& ecType) {
    return self.check(ecType);
})

// Good: pass by value, return tuple
.def("check", [](const Foo& self, SomeEnum::Type ecType) {
    bool result = self.check(ecType);
    return py::make_tuple(result, ecType);
})
```

### Abstract Base Classes

- Place ABCs in the `base` submodule via `manager.getSubmodule("base")`
- Use trampolines for classes with pure virtual methods
- Export concrete implementations to the main module

---

## Code Style

- **C++**: Follow the existing style (clang-format configuration coming soon)
- **Python**: Use ruff for linting tests

---

## Troubleshooting

### Settings.evaluationDate not persisting (Linux/macOS)

If `Settings.evaluationDate` changes don't persist across module boundaries, QuantLib was built as a shared library. The `Settings` singleton may exist in multiple instances due to Python's `RTLD_LOCAL` symbol loading.

**Solution**: Rebuild QuantLib as a static library with `-DBUILD_SHARED_LIBS=OFF -DCMAKE_POSITION_INDEPENDENT_CODE=ON`.

### "undefined symbol" or segmentation fault at import

This usually means QuantLib was built with `boost::shared_ptr` (the default) instead of `std::shared_ptr`. Rebuild QuantLib with `QL_USE_STD_SHARED_PTR=ON`.

### Link error: "mismatch detected for 'RuntimeLibrary'" (Windows)

If the build fails with errors like:
```
error LNK2038: mismatch detected for 'RuntimeLibrary': value 'MT_StaticRelease' doesn't match value 'MD_DynamicRelease'
```

This means QuantLib was built with the static runtime (`/MT`) but Python extensions require the dynamic runtime (`/MD`).

**Solution**: Rebuild QuantLib with `-DCMAKE_MSVC_RUNTIME_LIBRARY=MultiThreadedDLL`.

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
