/*
 * PyQuantLib: Python bindings for QuantLib
 * Copyright (c) 2025 Yassine Idyiahia
 * 
 * QuantLib is Copyright (c) 2000-2025 The QuantLib Authors
 * QuantLib is free software under a modified BSD license.
 * See http://quantlib.org/ for more information.
 * 
 * Source: https://github.com/quantales/pyquantlib
 * Licensed under the BSD 3-Clause License. See LICENSE file for details.
 */

#pragma once

#include <ql/quantlib.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/pytypes.h>
#include <pybind11/numpy.h> 

using namespace QuantLib;

namespace pybind11::detail {

/**
 * @brief Custom type caster for QuantLib::Array.
 * 
 * Enables automatic conversion between Python sequences/numpy arrays
 * and QuantLib::Array.
 */
template <> 
struct type_caster<QuantLib::Array> {
    PYBIND11_TYPE_CASTER(QuantLib::Array, _("Array"));

    // Conversion from Python to C++
    bool load(handle src, bool convert) {
        // Check if source is already a QuantLib::Array
        if (py::isinstance<QuantLib::Array>(src)) {
            value = py::cast<QuantLib::Array>(src);
            return true;
        }
        
        // Check if source is a numpy array
        if (py::isinstance<py::array>(src)) {
            auto np_arr = py::array_t<Real, py::array::c_style | py::array::forcecast>::ensure(src);
            if (!np_arr) return false;
            
            if (np_arr.ndim() != 1) {
                throw py::type_error("Expected 1-dimensional numpy array");
            }
            
            value = QuantLib::Array(np_arr.size());
            std::memcpy(value.begin(), np_arr.data(), np_arr.size() * sizeof(Real));
            return true;
        }
        
        // Check if source is any iterable (list, tuple, etc.)
        if (py::isinstance<py::iterable>(src)) {
            auto it = py::iter(src);
            std::vector<Real> temp;
            try {
                for (auto item : it) {
                    temp.push_back(item.cast<Real>());
                }
            } catch (py::cast_error&) {
                return false;
            }
            
            if (!temp.empty()) {
                value = QuantLib::Array(temp.begin(), temp.end());
            } else {
                value = QuantLib::Array();
            }
            return true;
        }
        
        return false;
    }

    // Conversion from C++ to Python
    static handle cast(const QuantLib::Array& src, return_value_policy policy, handle parent) {
        py::object arr = py::cast(src);
        return arr.release();
    }
};

} // namespace pybind11::detail
