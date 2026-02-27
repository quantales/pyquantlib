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
#include <ql/pricingengines/blackcalculator.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::blackcalculator(py::module_& m) {
    py::class_<BlackCalculator>(
        m, "BlackCalculator",
        "Black 1976 calculator for option pricing and Greeks.")
        .def(py::init<const ext::shared_ptr<StrikedTypePayoff>&,
                      Real, Real, Real>(),
            py::arg("payoff"),
            py::arg("forward"),
            py::arg("stdDev"),
            py::arg("discount") = 1.0,
            "Constructs from payoff, forward, stdDev, and discount.")
        .def(py::init<Option::Type, Real, Real, Real, Real>(),
            py::arg("optionType"),
            py::arg("strike"),
            py::arg("forward"),
            py::arg("stdDev"),
            py::arg("discount") = 1.0,
            "Constructs from option type, strike, forward, stdDev, and discount.")
        .def("value", &BlackCalculator::value,
            "Returns the option value.")
        .def("deltaForward", &BlackCalculator::deltaForward,
            "Sensitivity to change in the underlying forward price.")
        .def("delta", &BlackCalculator::delta,
            py::arg("spot"),
            "Sensitivity to change in the underlying spot price.")
        .def("elasticityForward", &BlackCalculator::elasticityForward,
            "Percent sensitivity to percent change in forward price.")
        .def("elasticity", &BlackCalculator::elasticity,
            py::arg("spot"),
            "Percent sensitivity to percent change in spot price.")
        .def("gammaForward", &BlackCalculator::gammaForward,
            "Second order derivative w.r.t. forward price.")
        .def("gamma", &BlackCalculator::gamma,
            py::arg("spot"),
            "Second order derivative w.r.t. spot price.")
        .def("theta", &BlackCalculator::theta,
            py::arg("spot"),
            py::arg("maturity"),
            "Sensitivity to time to maturity.")
        .def("thetaPerDay", &BlackCalculator::thetaPerDay,
            py::arg("spot"),
            py::arg("maturity"),
            "Sensitivity to time to maturity per day (365-day basis).")
        .def("vega", &BlackCalculator::vega,
            py::arg("maturity"),
            "Sensitivity to volatility.")
        .def("rho", &BlackCalculator::rho,
            py::arg("maturity"),
            "Sensitivity to discounting rate.")
        .def("dividendRho", &BlackCalculator::dividendRho,
            py::arg("maturity"),
            "Sensitivity to dividend/growth rate.")
        .def("itmCashProbability", &BlackCalculator::itmCashProbability,
            "Probability of being ITM in bond martingale measure, N(d2).")
        .def("itmAssetProbability", &BlackCalculator::itmAssetProbability,
            "Probability of being ITM in asset martingale measure, N(d1).")
        .def("strikeSensitivity", &BlackCalculator::strikeSensitivity,
            "Sensitivity to strike.")
        .def("strikeGamma", &BlackCalculator::strikeGamma,
            "Gamma w.r.t. strike.")
        .def("alpha", &BlackCalculator::alpha,
            "Returns alpha.")
        .def("beta", &BlackCalculator::beta,
            "Returns beta.");
}
