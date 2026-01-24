# Troubleshooting

Common issues and solutions when building or using PyQuantLib.

```{seealso}
{doc}`building` for complete build instructions.
```

## Build Issues

### Settings.evaluationDate not persisting (Linux/macOS)

**Symptom:** `Settings.evaluationDate` changes don't persist across module boundaries. Setting the date in one place doesn't affect calculations elsewhere.

**Cause:** QuantLib was built as a shared library. The `Settings` singleton uses a static local variable, which can exist in multiple instances when Python loads modules with `RTLD_LOCAL`.

**Solution:** Rebuild QuantLib as a static library:

```bash
cmake .. \
    -DBUILD_SHARED_LIBS=OFF \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
    -DQL_USE_STD_SHARED_PTR=ON
```

### "undefined symbol" or segmentation fault at import

**Symptom:** Import fails with undefined symbol errors or crashes immediately.

**Cause:** QuantLib was built with `boost::shared_ptr` (the default) instead of `std::shared_ptr`.

**Solution:** Rebuild QuantLib with:

```bash
cmake .. -DQL_USE_STD_SHARED_PTR=ON
```

Verify configuration:
```bash
grep "QL_USE_STD_SHARED_PTR" /usr/local/include/ql/config.hpp
# Should show: #define QL_USE_STD_SHARED_PTR
```

### CMake can't find QuantLib

**Symptom:** CMake error "Could not find QuantLib" or similar.

**Solution:** Set the `QL_DIR` environment variable:

```bash
# Windows
set QL_DIR=C:\QuantLib

# macOS/Linux
export QL_DIR=/usr/local
```

Or pass to CMake directly:
```bash
pip install -e . -C cmake.args="-DQL_DIR=/usr/local"
```

### Boost not found

**Symptom:** CMake error about missing Boost.

**Solution:** Ensure Boost is installed and hint CMake:

```bash
# Install (headers are sufficient)
# macOS:
brew install boost

# Ubuntu:
sudo apt-get install libboost-all-dev

# Windows (vcpkg):
vcpkg install boost:x64-windows

# Then hint CMake if needed:
pip install -e . -C cmake.args="-DBoost_ROOT=/path/to/boost"
```

### Build is slow

**Solution:** Enable parallel compilation:

```bash
# Windows PowerShell
$env:CMAKE_BUILD_PARALLEL_LEVEL = 8
pip install -e .

# macOS/Linux
CMAKE_BUILD_PARALLEL_LEVEL=8 pip install -e .
```

## Runtime Issues

### QuantLib error when discounting or computing prices

**Symptom:** Error like "discount date before reference date" or similar when calling `discount()`, `NPV()`, etc.

**Cause:** `Settings.evaluationDate` defaults to today's system date. If term structure or instrument dates don't align with this, QuantLib throws an error.

**Solution:** Always set `evaluationDate` explicitly at the start of the code:

```python
import pyquantlib as ql

today = ql.Date(15, 1, 2025)
ql.Settings.instance().evaluationDate = today

# Now all date-dependent calculations use this date
```

### "no day counter implementation provided"

**Symptom:** Error at import or when creating certain objects.

**Cause:** A binding used `DayCounter()` as a default argument, which creates an invalid object.

**Solution:** This is a bug in PyQuantLib. Please [report it](https://github.com/quantales/pyquantlib/issues). As a workaround, explicitly provide a day counter:

```python
# Instead of relying on default
curve = ql.FlatForward(today, 0.05)  # May fail

# Explicitly provide day counter
curve = ql.FlatForward(today, 0.05, ql.Actual365Fixed())  # Works
```

### "Tried to call pure virtual function" when pricing

**Symptom:** Runtime error when calling `NPV()` or other pricing methods:
```
RuntimeError: Tried to call pure virtual function "QuantLib::SomeEngine::calculate"
```

**Cause:** The pricing engine object was destroyed before `NPV()` was called. This happens when creating engines as temporaries (they get garbage collected immediately).

**Wrong approach:**
```python
# BAD - engine is destroyed before NPV() call
option.setPricingEngine(KirkEngine(process1, process2, correlation))
price = option.NPV()  # FAILS - engine is gone!
```

**Solution:** Keep the engine object alive:
```python
# GOOD - engine stays in scope
engine = KirkEngine(process1, process2, correlation)
option.setPricingEngine(engine)
price = option.NPV()  # Works!
```

This applies to **all pricing engines**, not just Python extensions. When `setPricingEngine()` is called, QuantLib stores a pointer to the engine, so the engine object must remain alive during pricing.

```{note}
This is a C++ object lifetime issue. Python's garbage collector doesn't know that QuantLib still needs the engine, so it destroys temporary objects immediately.
```

### Greeks return Null

**Symptom:** Greeks like `delta()` return `ql.QL_NULL_REAL` instead of a number.

**Possible causes:**
1. **Engine doesn't compute Greeks:** Some engines only compute NPV. For example, `AnalyticHestonEngine` doesn't compute Greeks: use finite difference engines instead.
2. **Option is too far OTM/ITM:** Numerical precision issues for extreme moneyness.

**Solution:** Check engine documentation or use a different engine.

### Can't switch to a different quote or term structure

**Symptom:** Need to replace a quote or term structure with a different object, but changes don't propagate.

**Cause:** Hidden handles don't support relinking to a different object.

**Solution:** Use relinkable handles when switching objects is needed:

```python
# Hidden handles: setValue() works, but can't switch objects
spot = ql.SimpleQuote(100.0)
process = ql.GeneralizedBlackScholesProcess(spot, ...)
spot.setValue(105.0)  # Works

# Relinkable handles: can switch to different objects
spot_handle = ql.RelinkableQuoteHandle(ql.SimpleQuote(100.0))
process = ql.GeneralizedBlackScholesProcess(spot_handle, ...)
spot_handle.linkTo(ql.SimpleQuote(105.0))  # Switch to new quote
```

See {doc}`handles` for more details.

### Memory issues with large calculations

**Symptom:** High memory usage or crashes during Monte Carlo or large term structure calculations.

**Solutions:**
1. Reduce `requiredSamples` for Monte Carlo
2. Use fewer time steps
3. Process in batches
4. Ensure no references to old objects are held

## Platform-Specific Issues

### Windows: "DLL load failed"

**Possible causes:**
1. Missing Visual C++ Redistributable
2. QuantLib DLL not in PATH (shouldn't happen with static build)
3. Architecture mismatch (32-bit vs 64-bit)

**Solutions:**
1. Install [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)
2. Ensure QuantLib was built as static (`-DBUILD_SHARED_LIBS=OFF`)
3. Match Python and QuantLib architectures (both x64 or both x86)

### macOS: "Library not loaded" or "symbol not found"

**Cause:** Usually means shared QuantLib library issues.

**Solution:** Ensure static build:
```bash
ls -la /usr/local/lib/libQuantLib*
# Should show libQuantLib.a (static)
# NOT libQuantLib.dylib (shared)
```

If `.dylib` appears, rebuild QuantLib with `-DBUILD_SHARED_LIBS=OFF`.

### Linux: Import hangs or crashes

**Cause:** Often singleton issues with shared library.

**Solution:** Same as macOS: rebuild as static library.

## Getting Help

If the issue isn't covered here:

1. Check [existing issues](https://github.com/quantales/pyquantlib/issues)
2. Search [QuantLib mailing list](https://sourceforge.net/projects/quantlib/lists/quantlib-users) for related QuantLib issues
3. [Open a new issue](https://github.com/quantales/pyquantlib/issues/new) with:
   - Python version (`python --version`)
   - OS and version
   - PyQuantLib version (`python -c "import pyquantlib as ql; print(ql.__version__)"`)
   - QuantLib version (`python -c "import pyquantlib as ql; print(ql.__ql_version__)"`)
   - Full error traceback
   - Minimal code to reproduce
