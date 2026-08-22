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
#include <ql/experimental/volatility/svismilesection.hpp>
#include <ql/experimental/volatility/sviinterpolation.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_experimental::svismilesection(py::module_& m) {
    // SviSmileSection - SVI parametric smile section
    py::classh<SviSmileSection, SmileSection>(
        m, "SviSmileSection",
        "Stochastic Volatility Inspired (SVI) smile section.\n\n"
        "The SVI total variance formula is:\n"
        "  w(k) = a + b * (rho * (k - m) + sqrt((k - m)^2 + sigma^2))\n"
        "where k = log(K/F) is the log-moneyness.\n\n"
        "Parameters (passed as vector [a, b, sigma, rho, m]):\n"
        "  a: vertical translation (level)\n"
        "  b: slope (must be >= 0)\n"
        "  sigma: ATM curvature (must be > 0)\n"
        "  rho: rotation (-1 < rho < 1)\n"
        "  m: horizontal translation")
        // Constructor with time
        .def(py::init<Time, Rate, std::vector<Real>>(),
            py::arg("timeToExpiry"),
            py::arg("forward"),
            py::arg("sviParameters"),
            "Constructs from time to expiry, forward, and SVI parameters [a, b, sigma, rho, m].")
        // Constructor with date
        .def(py::init<const Date&, Rate, std::vector<Real>, const DayCounter&>(),
            py::arg("expiryDate"),
            py::arg("forward"),
            py::arg("sviParameters"),
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs from expiry date, forward, SVI parameters [a, b, sigma, rho, m], and day counter.");

    // Helper functions from sviinterpolation.hpp
    m.def("sviTotalVariance", &detail::sviTotalVariance,
        py::arg("a"), py::arg("b"), py::arg("sigma"), py::arg("rho"), py::arg("m"), py::arg("k"),
        "Computes SVI total variance: a + b * (rho * (k - m) + sqrt((k - m)^2 + sigma^2)).\n\n"
        "Arguments:\n"
        "  a: vertical translation\n"
        "  b: slope\n"
        "  sigma: ATM curvature\n"
        "  rho: rotation\n"
        "  m: horizontal translation\n"
        "  k: log-moneyness (log(K/F))");

    m.def("checkSviParameters", &detail::checkSviParameters,
        py::arg("a"), py::arg("b"), py::arg("sigma"), py::arg("rho"), py::arg("m"), py::arg("tte"),
        "Validates SVI parameters for no-arbitrage conditions.\n\n"
        "Checks:\n"
        "  - b >= 0\n"
        "  - |rho| < 1\n"
        "  - sigma > 0\n"
        "  - a + b * sigma * sqrt(1 - rho^2) >= 0\n"
        "  - b * (1 + |rho|) <= 4");
}
