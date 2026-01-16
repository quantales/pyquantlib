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

#include "pyquantlib/pyquantlib.h"
#include "pyquantlib/null_utils.h"
#include <ql/utilities/null.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

namespace {
    // Null template class
    template <typename T>
    void bind_null(py::module& m, const std::string& name) {
        py::class_<Null<T>>(m, name.c_str())
            .def(py::init<>())
            .def("__int__", [](const Null<T>&) -> int { 
                if constexpr (std::is_integral_v<T>) {
                    return static_cast<int>(Null<T>());
                } else {
                    throw std::runtime_error("Cannot convert Null<Real> to int");
                }
            })
            .def("__float__", [](const Null<T>&) -> double { 
                if constexpr (std::is_floating_point_v<T>) {
                    return static_cast<double>(Null<T>());
                } else {
                    throw std::runtime_error("Cannot convert Null<Size> to float");
                }
            })
            .def("__repr__", [name](const Null<T>&) {
                return "Null<" + name + ">()";
            });
    }
}

// Null template instances
void ql_utilities::null(py::module_& m)
{
    bind_null<Size>(m, "NullSize");
    bind_null<Real>(m, "NullReal");
}