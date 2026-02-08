# Build QuantLib and Boost dependencies for Windows wheel builds.
# Called by cibuildwheel via CIBW_BEFORE_ALL_WINDOWS.
#
# Expects environment variables:
#   BOOST_VERSION       (e.g. "1.86.0")
#   QUANTLIB_VERSION    (e.g. "1.40")

$ErrorActionPreference = 'Stop'

# --- Boost headers ---
$BOOST_VERSION_UNDERSCORE = $env:BOOST_VERSION -replace '\.', '_'
Write-Host "Downloading Boost $env:BOOST_VERSION headers..."
Invoke-WebRequest -Uri "https://archives.boost.io/release/$env:BOOST_VERSION/source/boost_${BOOST_VERSION_UNDERSCORE}.zip" -OutFile boost.zip
Write-Host "Extracting Boost headers..."
Expand-Archive -Path boost.zip -DestinationPath C:/boost-temp
New-Item -ItemType Directory -Path C:/boost/include -Force | Out-Null
Move-Item "C:/boost-temp/boost_${BOOST_VERSION_UNDERSCORE}/boost" "C:/boost/include/boost"
Remove-Item -Recurse -Force C:/boost-temp, boost.zip
Write-Host "Boost headers installed to C:/boost/include"

# --- QuantLib ---
Write-Host "Downloading QuantLib $env:QUANTLIB_VERSION..."
Invoke-WebRequest -Uri "https://github.com/lballabio/QuantLib/releases/download/v$env:QUANTLIB_VERSION/QuantLib-$env:QUANTLIB_VERSION.tar.gz" -OutFile QuantLib.tar.gz
tar xzf QuantLib.tar.gz
Push-Location "QuantLib-$env:QUANTLIB_VERSION"
New-Item -ItemType Directory -Path build -Force | Out-Null
Push-Location build

Write-Host "Configuring QuantLib..."
cmake .. -G "Visual Studio 17 2022" -A x64 `
    -DCMAKE_BUILD_TYPE=Release `
    -DCMAKE_INSTALL_PREFIX=C:/quantlib `
    -DCMAKE_MSVC_RUNTIME_LIBRARY=MultiThreadedDLL `
    -DQL_USE_STD_SHARED_PTR=ON `
    -DQL_USE_STD_OPTIONAL=ON `
    -DQL_USE_STD_ANY=ON `
    -DQL_BUILD_EXAMPLES=OFF `
    -DQL_BUILD_TEST_SUITE=OFF `
    -DQL_BUILD_BENCHMARK=OFF `
    -DBoost_INCLUDE_DIR=C:/boost/include

Write-Host "Building QuantLib..."
cmake --build . --config Release --parallel

Write-Host "Installing QuantLib..."
cmake --install . --config Release

Pop-Location
Pop-Location
Remove-Item -Recurse -Force "QuantLib-$env:QUANTLIB_VERSION", QuantLib.tar.gz
Write-Host "QuantLib installed to C:/quantlib"
