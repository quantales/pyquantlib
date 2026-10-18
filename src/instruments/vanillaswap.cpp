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
#include <ql/instruments/vanillaswap.hpp>
#include <ql/indexes/iborindex.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::vanillaswap(py::module_& m) {
    // VanillaSwap class
    py::class_<VanillaSwap, FixedVsFloatingSwap, ext::shared_ptr<VanillaSwap>>(
        m, "VanillaSwap",
        "Plain vanilla swap: fixed vs IBOR floating leg.")
        .def(py::init<Swap::Type, Real, Schedule, Rate, DayCounter,
                      Schedule, ext::shared_ptr<IborIndex>, Spread, DayCounter,
                      std::optional<BusinessDayConvention>,
                      std::optional<bool>>(),
            py::arg("type"),
            py::arg("nominal"),
            py::arg("fixedSchedule"),
            py::arg("fixedRate"),
            py::arg("fixedDayCount"),
            py::arg("floatSchedule"),
            py::arg("iborIndex"),
            py::arg("spread"),
            py::arg("floatingDayCount"),
            py::arg("paymentConvention") = std::nullopt,
            py::arg("useIndexedCoupons") = std::nullopt,
            "Constructs a vanilla swap.");
}
