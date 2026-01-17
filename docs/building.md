# Building from Source

This guide covers building QuantLib and PyQuantLib from source.

## Build System

PyQuantLib uses [scikit-build-core](https://github.com/scikit-build/scikit-build-core), a modern Python build backend that integrates CMake with Python packaging.

### Why scikit-build-core?

- **PEP 517 compliant**: Works with `pip install`, `python -m build`, and modern tooling
- **CMake integration**: Native support for C++ projects
- **Automatic dependency handling**: Finds pybind11, QuantLib via CMake
- **Cross-platform**: Consistent builds on Windows, macOS, Linux

### Configuration

Build settings are in `pyproject.toml`:

```toml
[build-system]
requires = ["scikit-build-core>=0.10.0", "pybind11>=2.11.0"]
build-backend = "scikit_build_core.build"

[tool.scikit-build]
build-dir = "build"
cmake.version = ">=3.18"
cmake.build-type = "Release"
wheel.packages = ["pyquantlib"]
```

### CMake Presets

For IDE integration and manual builds, `CMakePresets.json` provides development presets:

```bash
# Configure (auto-selects dev-windows or dev-unix)
cmake --preset dev-windows  # or dev-unix

# Build
cmake --build --preset dev-windows
```

Presets auto-detect the virtual environment Python.

## QuantLib Requirements

```{important}
PyQuantLib requires QuantLib built as a **static library** with `std::shared_ptr`. Pre-built packages (Homebrew, vcpkg, apt) are **not compatible**.
```

### Required CMake Flags

```bash
cmake .. \
    -DBUILD_SHARED_LIBS=OFF \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
    -DQL_USE_STD_SHARED_PTR=ON \
    -DCMAKE_BUILD_TYPE=Release
```

### Why These Flags?

- **`BUILD_SHARED_LIBS=OFF`**: Static build prevents Settings singleton issues on Linux/macOS. QuantLib's `Settings` singleton uses a static local variable. When QuantLib is a shared library, Python loads modules with `RTLD_LOCAL`, which can cause the singleton to exist in multiple instances.
- **`CMAKE_POSITION_INDEPENDENT_CODE=ON`**: Required for static libs in Python modules.
- **`QL_USE_STD_SHARED_PTR=ON`**: pybind11 uses `std::shared_ptr` as default holder.

## Building QuantLib

### Download

```bash
# Download release
wget https://github.com/lballabio/QuantLib/releases/download/v1.40/QuantLib-1.40.tar.gz
tar xzf QuantLib-1.40.tar.gz
cd QuantLib-1.40

# Or clone
git clone https://github.com/lballabio/QuantLib.git
cd QuantLib
git checkout v1.40
```

### Windows

**Prerequisites:**
- Visual Studio 2019 or later
- Boost (headers only)

```powershell
# Install Boost via vcpkg
vcpkg install boost:x64-windows

# Configure
mkdir build && cd build
cmake .. -G "Visual Studio 16 2019" -A x64 ^
    -DBUILD_SHARED_LIBS=OFF ^
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON ^
    -DQL_USE_STD_SHARED_PTR=ON ^
    -DCMAKE_BUILD_TYPE=Release ^
    -DCMAKE_INSTALL_PREFIX=C:/QuantLib ^
    -DBoost_ROOT=C:/vcpkg/installed/x64-windows

# Build and install
cmake --build . --config Release --parallel 8
cmake --install . --config Release

# Set environment variable
set QL_DIR=C:\QuantLib
```

### macOS

**Prerequisites:**
```bash
brew install boost cmake
```

**Build:**
```bash
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

**Build:**
```bash
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

### Verify QuantLib

```bash
# Check config.hpp
grep -E "QL_USE_STD_(SHARED_PTR|OPTIONAL|ANY)" /usr/local/include/ql/config.hpp

# Should show .a files (static), not .so/.dylib (shared)
ls -la /usr/local/lib/libQuantLib*
```

Expected output:
```
libQuantLib.a          # Correct (static)
# NOT libQuantLib.so   # Wrong (shared)
```

## Building PyQuantLib

### From Source

```bash
git clone https://github.com/quantales/pyquantlib.git
cd pyquantlib

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install -r requirements-dev.txt
pip install -e .
```

### Parallel Builds

```bash
# Windows PowerShell
$env:CMAKE_BUILD_PARALLEL_LEVEL = 8
pip install -e .

# macOS/Linux
CMAKE_BUILD_PARALLEL_LEVEL=8 pip install -e .
```

### Verify Installation

```bash
python -c "import pyquantlib as ql; print(f'PyQuantLib {ql.__version__}')"
```

## Building Documentation

```bash
# Install docs dependencies
pip install -e ".[docs]"

# Build
python scripts/build_docs.py

# Build and open in browser
python scripts/build_docs.py --open
```

Or manually:

```bash
cd docs
sphinx-build -b html . _build/html
```

## Building Wheels

```bash
python -m build
# Output in dist/
```

## Troubleshooting

### QuantLib Not Found

CMake looks for QuantLib in standard locations. If not found, set one of:

```bash
# Environment variable
export QL_DIR=/path/to/quantlib
pip install -e .

# Or CMake variable
CMAKE_ARGS="-DQuantLib_ROOT=/path/to/quantlib" pip install -e .
```

### Wrong QuantLib Version

If you have multiple QuantLib installations, ensure the static build is found first:

```bash
# Check which QuantLib is found
cmake -S . -B build 2>&1 | grep -i quantlib
```

### Build Errors

Common issues:

- **"QL_USE_STD_SHARED_PTR not defined"**: Rebuild QuantLib with `-DQL_USE_STD_SHARED_PTR=ON`
- **"undefined reference to Settings"**: QuantLib was built as shared library; rebuild as static
- **"Python.h not found"**: Ensure Python dev headers are installed (`python3-dev` on Linux)
