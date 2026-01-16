# Installation

## Prerequisites

Before building, ensure the following are installed:

- **Python 3.9+**
- **CMake 3.18+**
- **C++17 compatible compiler**
  - Windows: MSVC 2019+ (Visual Studio 2019 or later)
  - macOS: Xcode 12+ or clang 10+
  - Linux: GCC 9+ or clang 10+
- **Boost headers** (required by QuantLib)
- **QuantLib 1.40+** built with specific configuration (see below)

## QuantLib Build Requirements

```{important}
PyQuantLib requires QuantLib built as a **static library** with `std::shared_ptr`. Pre-built packages (Homebrew, vcpkg, apt) are **not compatible** and QuantLib must be built from source.
```

### Why These Requirements?

| Flag | Value | Reason |
|------|-------|--------|
| `BUILD_SHARED_LIBS` | `OFF` | Static build prevents Settings singleton issues on Linux/macOS |
| `CMAKE_POSITION_INDEPENDENT_CODE` | `ON` | Required for static libs in Python modules |
| `QL_USE_STD_SHARED_PTR` | `ON` | pybind11 uses `std::shared_ptr` as default holder |

**Why static builds?** QuantLib's `Settings` singleton uses a static local variable. When QuantLib is a shared library, Python loads modules with `RTLD_LOCAL`, which can cause the singleton to exist in multiple instances. Static linking embeds QuantLib into the Python module, ensuring a single singleton instance.

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

Expected `config.hpp` output:
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

## Installing PyQuantLib

### From Source (Recommended)

```bash
# After building QuantLib with required flags
pip install git+https://github.com/quantales/pyquantlib.git
```

### Development Installation

```bash
# Clone the repository
git clone https://github.com/quantales/pyquantlib.git
cd pyquantlib

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies and build
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
pip install -e .

# Verify installation
python -c "import pyquantlib as ql; print(f'PyQuantLib {ql.__version__}')"
```

### Parallel Builds

Ninja auto-detects CPU cores. To override:

```bash
# Windows PowerShell
$env:CMAKE_BUILD_PARALLEL_LEVEL = 8
pip install -e .

# macOS/Linux
CMAKE_BUILD_PARALLEL_LEVEL=8 pip install -e .
```
