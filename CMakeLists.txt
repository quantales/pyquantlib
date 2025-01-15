# pyquantlib - Python bindings for QuantLib
# Copyright (C) 2025 Yassine Idyiahia
#
# Source: https://github.com/quantales/pyquantlib
# Licensed under the BSD 3-Clause License. See LICENSE file for details.

cmake_minimum_required(VERSION 3.18)
project(pyquantlib
    LANGUAGES CXX
    DESCRIPTION "Python bindings for QuantLib"
)

# ==============================================================================
# Build Configuration
# ==============================================================================

# C++17 is required (QuantLib 1.31+ requirement, pybind11 best practice)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Default to Release build
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS
        "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")

# ==============================================================================
# Options
# ==============================================================================

option(PYQUANTLIB_DETAILED_ERRORS "Enable detailed pybind11 error messages" ON)

# ==============================================================================
# Version from pyproject.toml
# ==============================================================================

file(READ "${CMAKE_SOURCE_DIR}/pyproject.toml" PYPROJECT_CONTENTS)
string(REGEX MATCH "version *= *\"([0-9]+\\.[0-9]+\\.[0-9]+)\"" _ "${PYPROJECT_CONTENTS}")
set(PYQUANTLIB_VERSION "${CMAKE_MATCH_1}")

if(NOT PYQUANTLIB_VERSION)
    message(WARNING "Could not parse version from pyproject.toml, using 0.0.0")
    set(PYQUANTLIB_VERSION "0.0.0")
endif()

message(STATUS "PyQuantLib version: ${PYQUANTLIB_VERSION}")

# ==============================================================================
# Dependencies: Python and pybind11
# ==============================================================================

find_package(Python3 REQUIRED COMPONENTS Interpreter Development.Module)
message(STATUS "Python: ${Python3_EXECUTABLE} (${Python3_VERSION})")

find_package(pybind11 CONFIG REQUIRED)
message(STATUS "pybind11: ${pybind11_VERSION}")

# ==============================================================================
# Dependencies: Boost (headers only - required by QuantLib)
# ==============================================================================

# Boost discovery order:
# 1. CMake argument: -DBOOST_ROOT=/path/to/boost
# 2. Environment variable: BOOST_ROOT
# 3. vcpkg toolchain (automatic if CMAKE_TOOLCHAIN_FILE is set)
# 4. System paths (brew on macOS, apt/dnf packages on Linux)

if(NOT DEFINED BOOST_ROOT AND DEFINED ENV{BOOST_ROOT})
    set(BOOST_ROOT "$ENV{BOOST_ROOT}")
endif()

# We only need Boost headers (QuantLib links Boost if needed)
find_package(Boost 1.75.0 REQUIRED)

if(Boost_FOUND)
    message(STATUS "Boost: ${Boost_VERSION} (${Boost_INCLUDE_DIRS})")
else()
    message(FATAL_ERROR
        "Boost not found. Install Boost or set BOOST_ROOT:\n"
        "  cmake -DBOOST_ROOT=/path/to/boost ..\n"
        "  or: export BOOST_ROOT=/path/to/boost"
    )
endif()

# ==============================================================================
# Dependencies: QuantLib
# ==============================================================================

# QuantLib discovery order:
# 1. CMake argument: -DQuantLib_ROOT=/path/to/quantlib
# 2. Environment variable: QuantLib_ROOT or QL_DIR
# 3. vcpkg toolchain (automatic if CMAKE_TOOLCHAIN_FILE is set)
# 4. System paths (brew on macOS, apt/dnf packages on Linux)
# 5. Manual fallback for source builds without CMake config

# Support legacy QL_DIR environment variable
if(NOT DEFINED QuantLib_ROOT)
    if(DEFINED ENV{QuantLib_ROOT})
        set(QuantLib_ROOT "$ENV{QuantLib_ROOT}")
    elseif(DEFINED ENV{QL_DIR})
        set(QuantLib_ROOT "$ENV{QL_DIR}")
    endif()
endif()

# First, try standard CMake find_package (works for vcpkg, brew, system packages)
find_package(QuantLib 1.30 QUIET CONFIG)

if(QuantLib_FOUND)
    message(STATUS "QuantLib: ${QuantLib_VERSION} (found via CMake config)")
    set(QUANTLIB_TARGET QuantLib::QuantLib)
else()
    # Fallback: Manual detection for source builds without QuantLibConfig.cmake
    message(STATUS "QuantLib CMake config not found, trying manual detection...")
    
    if(NOT QuantLib_ROOT)
        message(FATAL_ERROR
            "QuantLib not found. Set QuantLib_ROOT or QL_DIR:\n"
            "  cmake -DQuantLib_ROOT=/path/to/quantlib ..\n"
            "  or: set QL_DIR environment variable\n"
            "  or: set QuantLib_ROOT environment variable"
        )
    endif()
    
    # Find headers
    find_path(QuantLib_INCLUDE_DIR
        NAMES ql/quantlib.hpp
        PATHS 
            "${QuantLib_ROOT}/include"
            "${QuantLib_ROOT}"
        NO_DEFAULT_PATH
    )
    
    if(NOT QuantLib_INCLUDE_DIR)
        message(FATAL_ERROR
            "QuantLib headers not found at ${QuantLib_ROOT}\n"
            "Expected to find: ${QuantLib_ROOT}/include/ql/quantlib.hpp or ${QuantLib_ROOT}/ql/quantlib.hpp"
        )
    endif()
    
    # Find library - handle different naming conventions
    if(WIN32)
        # Windows: QuantLib-x64-mt.lib (Release) or QuantLib-x64-mt-gd.lib (Debug)
        if(CMAKE_BUILD_TYPE STREQUAL "Debug")
            set(_ql_lib_names QuantLib-x64-mt-gd QuantLib-x64-mt QuantLib)
        else()
            set(_ql_lib_names QuantLib-x64-mt QuantLib)
        endif()
    else()
        # Unix: libQuantLib.a or libQuantLib.so
        set(_ql_lib_names QuantLib)
    endif()
    
    find_library(QuantLib_LIBRARY
        NAMES ${_ql_lib_names}
        PATHS 
            "${QuantLib_ROOT}/lib"
            "${QuantLib_ROOT}/lib64"
            "${QuantLib_ROOT}/lib/x86_64-linux-gnu"
            "${QuantLib_ROOT}/build/ql"
            "${QuantLib_ROOT}/build/ql/Release"
        NO_DEFAULT_PATH
    )
    
    if(NOT QuantLib_LIBRARY)
        message(FATAL_ERROR
            "QuantLib library not found.\n"
            "Searched for: ${_ql_lib_names}\n"
            "In paths: ${QuantLib_ROOT}/lib, ${QuantLib_ROOT}/build/ql"
        )
    endif()
    
    # Create imported target for consistency
    add_library(QuantLib::QuantLib UNKNOWN IMPORTED)
    set_target_properties(QuantLib::QuantLib PROPERTIES
        IMPORTED_LOCATION "${QuantLib_LIBRARY}"
        INTERFACE_INCLUDE_DIRECTORIES "${QuantLib_INCLUDE_DIR}"
    )
    
    message(STATUS "QuantLib: manual detection")
    message(STATUS "  Headers: ${QuantLib_INCLUDE_DIR}")
    message(STATUS "  Library: ${QuantLib_LIBRARY}")
    set(QUANTLIB_TARGET QuantLib::QuantLib)
endif()

# ==============================================================================
# Source Files
# ==============================================================================

file(GLOB_RECURSE PYQUANTLIB_SOURCES CONFIGURE_DEPENDS
    "${CMAKE_SOURCE_DIR}/src/*.cpp"
)

file(GLOB_RECURSE PYQUANTLIB_HEADERS CONFIGURE_DEPENDS
    "${CMAKE_SOURCE_DIR}/include/*.h"
    "${CMAKE_SOURCE_DIR}/include/*.hpp"
)

# IDE source grouping (Visual Studio, Xcode)
source_group(TREE "${CMAKE_SOURCE_DIR}/src" PREFIX "Source Files" FILES ${PYQUANTLIB_SOURCES})
source_group(TREE "${CMAKE_SOURCE_DIR}/include" PREFIX "Header Files" FILES ${PYQUANTLIB_HEADERS})

# ==============================================================================
# Build Target
# ==============================================================================

pybind11_add_module(_pyquantlib MODULE ${PYQUANTLIB_SOURCES} ${PYQUANTLIB_HEADERS})

target_include_directories(_pyquantlib PRIVATE
    "${CMAKE_SOURCE_DIR}/include"
)

target_link_libraries(_pyquantlib PRIVATE
    ${QUANTLIB_TARGET}
    Boost::headers
)

# Compile definitions
if(PYQUANTLIB_DETAILED_ERRORS)
    target_compile_definitions(_pyquantlib PRIVATE PYBIND11_DETAILED_ERROR_MESSAGES)
endif()

# ==============================================================================
# Platform-Specific Configuration
# ==============================================================================

if(MSVC)
    # Windows/MSVC specific settings
    target_compile_options(_pyquantlib PRIVATE
        /W4             # Warning level 4
        /MP             # Multi-processor compilation
        /utf-8          # UTF-8 source and execution character set
    )
    target_compile_definitions(_pyquantlib PRIVATE
        _CRT_SECURE_NO_WARNINGS
        NOMINMAX        # Prevent Windows.h from defining min/max macros
    )
elseif(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    # GCC/Clang settings
    target_compile_options(_pyquantlib PRIVATE
        -Wall
        -Wextra
        -Wpedantic
    )
endif()

# ==============================================================================
# Installation
# ==============================================================================

# Install the Python extension module
install(TARGETS _pyquantlib
    LIBRARY DESTINATION pyquantlib
    COMPONENT python
)

# ==============================================================================
# Development Convenience: Copy to Source Tree
# ==============================================================================

# For development (pip install -e .), copy the built module to the source tree
# This allows importing without reinstalling after each build
add_custom_command(TARGET _pyquantlib POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "$<TARGET_FILE:_pyquantlib>"
        "${CMAKE_SOURCE_DIR}/pyquantlib/$<TARGET_FILE_NAME:_pyquantlib>"
    COMMENT "Copying _pyquantlib to source tree for development..."
    VERBATIM
)

# ==============================================================================
# Summary
# ==============================================================================

message(STATUS "")
message(STATUS "PyQuantLib Configuration Summary")
message(STATUS "================================")
message(STATUS "  Version:      ${PYQUANTLIB_VERSION}")
message(STATUS "  Build type:   ${CMAKE_BUILD_TYPE}")
message(STATUS "  C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "  Python:       ${Python3_VERSION}")
message(STATUS "  pybind11:     ${pybind11_VERSION}")
message(STATUS "  Boost:        ${Boost_VERSION}")
if(QuantLib_VERSION)
    message(STATUS "  QuantLib:     ${QuantLib_VERSION}")
else()
    message(STATUS "  QuantLib:     (manual detection)")
endif()
message(STATUS "")
