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
#include <ql/pricingengines/bacheliercalculator.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::bacheliercalculator(py::module_& m) {
    py::class_<BachelierCalculator>(
        m, "BachelierCalculator",
        "Bachelier (normal-volatility) calculator for option pricing and Greeks.")
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
        .def("value", &BachelierCalculator::value,
            "Returns the option value.")
        .def("deltaForward", &BachelierCalculator::deltaForward,
            "Sensitivity to change in the underlying forward price.")
        .def("delta", &BachelierCalculator::delta,
            py::arg("spot"),
            "Sensitivity to change in the underlying spot price.")
        .def("elasticityForward", &BachelierCalculator::elasticityForward,
            "Percent sensitivity to percent change in forward price.")
        .def("elasticity", &BachelierCalculator::elasticity,
            py::arg("spot"),
            "Percent sensitivity to percent change in spot price.")
        .def("gammaForward", &BachelierCalculator::gammaForward,
            "Second order derivative w.r.t. forward price.")
        .def("gamma", &BachelierCalculator::gamma,
            py::arg("spot"),
            "Second order derivative w.r.t. spot price.")
        .def("theta", &BachelierCalculator::theta,
            py::arg("spot"),
            py::arg("maturity"),
            "Sensitivity to time to maturity.")
        .def("thetaPerDay", &BachelierCalculator::thetaPerDay,
            py::arg("spot"),
            py::arg("maturity"),
            "Sensitivity to time to maturity per day (365-day basis).")
        .def("vega", &BachelierCalculator::vega,
            py::arg("maturity"),
            "Sensitivity to volatility.")
        .def("rho", &BachelierCalculator::rho,
            py::arg("maturity"),
            "Sensitivity to discounting rate.")
        .def("dividendRho", &BachelierCalculator::dividendRho,
            py::arg("maturity"),
            "Sensitivity to dividend/growth rate.")
        .def("itmCashProbability", &BachelierCalculator::itmCashProbability,
            "Probability of being ITM in bond martingale measure.")
        .def("itmAssetProbability", &BachelierCalculator::itmAssetProbability,
            "Probability of being ITM in asset martingale measure.")
        .def("strikeSensitivity", &BachelierCalculator::strikeSensitivity,
            "Sensitivity to strike.")
        .def("strikeGamma", &BachelierCalculator::strikeGamma,
            "Gamma w.r.t. strike.")
        .def("alpha", &BachelierCalculator::alpha,
            "Returns alpha.")
        .def("beta", &BachelierCalculator::beta,
            "Returns beta.");
}
