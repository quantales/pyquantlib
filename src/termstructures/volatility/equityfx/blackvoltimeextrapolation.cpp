/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2026 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is Copyright (c) 2000-2026 The QuantLib Authors
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/termstructures/volatility/equityfx/blackvoltimeextrapolation.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::blackvoltimeextrapolation(py::module_& m) {
    auto cls = py::class_<BlackVolTimeExtrapolation>(
        m, "BlackVolTimeExtrapolation",
        "Time-extrapolation strategies for Black volatility term structures.");

    py::enum_<BlackVolTimeExtrapolation::Type>(cls, "Type",
        "Time-extrapolation strategy for Black volatility.")
        .value("FlatVolatility", BlackVolTimeExtrapolation::FlatVolatility)
        .value("UseInterpolator", BlackVolTimeExtrapolation::UseInterpolator)
        .value("LinearVariance", BlackVolTimeExtrapolation::LinearVariance)
        .export_values();
}
