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
#include <ql/compounding.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;

void ql_core::compounding(py::module_& m) {
    py::enum_<QuantLib::Compounding>(m, "Compounding", py::arithmetic(),
        "Interest rate compounding rule.")
        .value("Simple", QuantLib::Simple, "1 + r*t")
        .value("Compounded", QuantLib::Compounded, "(1 + r)^t")
        .value("Continuous", QuantLib::Continuous, "e^(r*t)")
        .value("SimpleThenCompounded", QuantLib::SimpleThenCompounded,
            "Simple up to the first period, then Compounded.")
        .value("CompoundedThenSimple", QuantLib::CompoundedThenSimple,
            "Compounded up to the first period, then Simple.")
        .export_values();
}
