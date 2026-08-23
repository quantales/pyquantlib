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
#include <ql/cashflows/duration.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::duration(py::module_& m) {
    py::enum_<Duration::Type>(m, "DurationType",
        "Duration calculation type.")
        .value("Simple", Duration::Simple, "Simple duration.")
        .value("Macaulay", Duration::Macaulay, "Macaulay duration.")
        .value("Modified", Duration::Modified, "Modified duration.");
}
