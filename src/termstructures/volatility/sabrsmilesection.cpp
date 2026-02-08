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
#include <ql/termstructures/volatility/sabrsmilesection.hpp>
#include <ql/termstructures/volatility/sabr.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::sabrsmilesection(py::module_& m) {
    py::class_<SabrSmileSection, SmileSection, ext::shared_ptr<SabrSmileSection>>(
        m, "SabrSmileSection",
        "SABR parametric smile section.")
        .def(py::init<Time, Rate, const std::vector<Real>&, Real, VolatilityType>(),
            py::arg("timeToExpiry"),
            py::arg("forward"),
            py::arg("sabrParameters"),
            py::arg("shift") = 0.0,
            py::arg("volatilityType") = VolatilityType::ShiftedLognormal,
            "Constructs from time to expiry, forward, and SABR parameters [alpha, beta, nu, rho].")
        .def(py::init<const Date&, Rate, const std::vector<Real>&,
                       const Date&, const DayCounter&, Real, VolatilityType>(),
            py::arg("expiryDate"),
            py::arg("forward"),
            py::arg("sabrParameters"),
            py::arg("referenceDate") = Date(),
            py::arg("dayCounter") = Actual365Fixed(),
            py::arg("shift") = 0.0,
            py::arg("volatilityType") = VolatilityType::ShiftedLognormal,
            "Constructs from expiry date, forward, and SABR parameters [alpha, beta, nu, rho].")
        .def("alpha", &SabrSmileSection::alpha, "Returns SABR alpha parameter.")
        .def("beta", &SabrSmileSection::beta, "Returns SABR beta parameter.")
        .def("nu", &SabrSmileSection::nu, "Returns SABR nu parameter.")
        .def("rho", &SabrSmileSection::rho, "Returns SABR rho parameter.");

    // SABR formula free functions
    m.def("sabrVolatility", &sabrVolatility,
        py::arg("strike"), py::arg("forward"), py::arg("expiryTime"),
        py::arg("alpha"), py::arg("beta"), py::arg("nu"), py::arg("rho"),
        py::arg("volatilityType") = VolatilityType::ShiftedLognormal,
        "Computes SABR implied volatility (with parameter validation).");

    m.def("shiftedSabrVolatility", &shiftedSabrVolatility,
        py::arg("strike"), py::arg("forward"), py::arg("expiryTime"),
        py::arg("alpha"), py::arg("beta"), py::arg("nu"), py::arg("rho"),
        py::arg("shift"),
        py::arg("volatilityType") = VolatilityType::ShiftedLognormal,
        "Computes shifted SABR implied volatility.");

    m.def("validateSabrParameters", &validateSabrParameters,
        py::arg("alpha"), py::arg("beta"), py::arg("nu"), py::arg("rho"),
        "Validates SABR parameters (raises on invalid).");
}
