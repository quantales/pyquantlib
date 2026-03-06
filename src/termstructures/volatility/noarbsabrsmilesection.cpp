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
#include <ql/experimental/volatility/noarbsabrsmilesection.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::noarbsabrsmilesection(py::module_& m) {
    py::class_<NoArbSabrSmileSection, SmileSection,
               ext::shared_ptr<NoArbSabrSmileSection>>(
        m, "NoArbSabrSmileSection",
        "No-arbitrage SABR smile section. Wraps NoArbSabrModel to provide "
        "a SmileSection interface.")
        // Time-based constructor
        .def(py::init<Time, Rate, std::vector<Real>, Real, VolatilityType>(),
            py::arg("timeToExpiry"),
            py::arg("forward"),
            py::arg("sabrParameters"),
            py::arg("shift") = 0.0,
            py::arg("volatilityType") = VolatilityType::ShiftedLognormal,
            "Constructs from time to expiry, forward, and SABR parameters "
            "[alpha, beta, nu, rho].")
        // Date-based constructor
        .def(py::init<const Date&, Rate, std::vector<Real>,
                       const DayCounter&, Real, VolatilityType>(),
            py::arg("expiryDate"),
            py::arg("forward"),
            py::arg("sabrParameters"),
            py::arg("dayCounter") = Actual365Fixed(),
            py::arg("shift") = 0.0,
            py::arg("volatilityType") = VolatilityType::ShiftedLognormal,
            "Constructs from expiry date, forward, and SABR parameters "
            "[alpha, beta, nu, rho].")
        .def("model", &NoArbSabrSmileSection::model,
            "Returns the underlying NoArbSabrModel.");
}
