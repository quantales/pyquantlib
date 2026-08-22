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
#include <ql/instruments/futures.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::futures(py::module_& m) {
    py::enum_<Futures::Type>(m, "Futures",
        "Futures date-rule conventions.")
        .value("IMM", Futures::IMM,
               "Third Wednesday of March, June, September, December.")
        .value("ASX", Futures::ASX,
               "Second Friday of March, June, September, December.")
        .value("Custom", Futures::Custom, "Other rules.")
        .export_values();
}
