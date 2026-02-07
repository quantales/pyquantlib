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
#include <ql/cashflows/rateaveraging.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::rateaveraging(py::module_& m) {
    py::class_<RateAveraging> rateAvg(m, "RateAveraging",
        "Rate averaging methods for multi-fixing coupons.");
    py::enum_<RateAveraging::Type>(rateAvg, "Type",
        "Rate averaging type.")
        .value("Simple", RateAveraging::Simple,
            "Simple averaging: sum of sub-period interest amounts.")
        .value("Compound", RateAveraging::Compound,
            "Compound averaging: compounded sub-period rates.");
}
