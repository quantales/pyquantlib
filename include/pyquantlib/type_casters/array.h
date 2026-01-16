/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is Copyright (c) 2000-2025 The QuantLib Authors
 * https://www.quantlib.org/
 */

#pragma once

#include <ql/math/array.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <cstring>

namespace pybind11::detail {

/**
 * Custom type caster for QuantLib::Array.
 * Enables automatic conversion between Python sequences/numpy arrays
 * and QuantLib::Array.
 */
template <>
struct type_caster<QuantLib::Array> {
    PYBIND11_TYPE_CASTER(QuantLib::Array, _("Array"));

    // Python to C++
    bool load(handle src, bool /*convert*/) {
        // Already a QuantLib::Array
        if (py::isinstance<QuantLib::Array>(src)) {
            value = py::cast<QuantLib::Array>(src);
            return true;
        }

        // NumPy array
        if (py::isinstance<py::array>(src)) {
            auto np_arr = py::array_t<QuantLib::Real,
                py::array::c_style | py::array::forcecast>::ensure(src);
            if (!np_arr) return false;
            if (np_arr.ndim() != 1) {
                throw py::type_error("Expected 1-dimensional numpy array");
            }
            value = QuantLib::Array(np_arr.size());
            std::memcpy(value.begin(), np_arr.data(),
                np_arr.size() * sizeof(QuantLib::Real));
            return true;
        }

        // Any iterable (list, tuple, etc.)
        if (py::isinstance<py::iterable>(src)) {
            std::vector<QuantLib::Real> temp;
            try {
                for (auto item : py::iter(src)) {
                    temp.push_back(item.cast<QuantLib::Real>());
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

    // C++ to Python
    static handle cast(const QuantLib::Array& src,
                       return_value_policy /*policy*/, handle /*parent*/) {
        return py::cast(src).release();
    }
};

} // namespace pybind11::detail
