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

#include "pyquantlib/pyquantlib.h"
#include <ql/types.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;

void ql_core::constants(py::module_& m) {
    m.attr("MIN_INTEGER") = QL_MIN_INTEGER;
    m.attr("MAX_INTEGER") = QL_MAX_INTEGER;
    m.attr("MIN_REAL") = QL_MIN_REAL;
    m.attr("MAX_REAL") = QL_MAX_REAL;
    m.attr("MIN_POSITIVE_REAL") = QL_MIN_POSITIVE_REAL;
    m.attr("EPSILON") = QL_EPSILON;
}
