/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
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
