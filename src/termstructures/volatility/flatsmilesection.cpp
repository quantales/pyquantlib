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
#include <ql/termstructures/volatility/flatsmilesection.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::flatsmilesection(py::module_& m) {
    py::class_<FlatSmileSection, SmileSection,
               ext::shared_ptr<FlatSmileSection>>(
        m, "FlatSmileSection",
        "Smile section with constant volatility.")
        .def(py::init([](const Date& d, Volatility vol,
                         const DayCounter& dc, const Date& referenceDate,
                         const py::object& atmLevel,
                         VolatilityType type, Real shift) {
            Real atm = atmLevel.is_none() ? Null<Rate>()
                                          : atmLevel.cast<Real>();
            return ext::make_shared<FlatSmileSection>(
                d, vol, dc, referenceDate, atm, type, shift);
        }),
            py::arg("d"),
            py::arg("vol"),
            py::arg("dc") = Actual365Fixed(),
            py::arg("referenceDate") = Date(),
            py::arg("atmLevel") = py::none(),
            py::arg("type") = ShiftedLognormal,
            py::arg("shift") = 0.0,
            "Constructs with exercise date.")
        .def(py::init([](Time exerciseTime, Volatility vol,
                         const DayCounter& dc,
                         const py::object& atmLevel,
                         VolatilityType type, Real shift) {
            Real atm = atmLevel.is_none() ? Null<Rate>()
                                          : atmLevel.cast<Real>();
            return ext::make_shared<FlatSmileSection>(
                exerciseTime, vol, dc, atm, type, shift);
        }),
            py::arg("exerciseTime"),
            py::arg("vol"),
            py::arg("dc") = Actual365Fixed(),
            py::arg("atmLevel") = py::none(),
            py::arg("type") = ShiftedLognormal,
            py::arg("shift") = 0.0,
            "Constructs with exercise time.");
}
