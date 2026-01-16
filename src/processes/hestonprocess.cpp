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
#include <ql/processes/hestonprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_processes::hestonprocess(py::module_& m) {
    auto cls = py::class_<HestonProcess, StochasticProcess,
                          ext::shared_ptr<HestonProcess>>(
        m, "HestonProcess",
        "Heston stochastic volatility process.");

    // Discretization enum
    py::enum_<HestonProcess::Discretization>(cls, "Discretization",
        "Discretization schemes for Heston process simulation.")
        .value("PartialTruncation", HestonProcess::PartialTruncation)
        .value("FullTruncation", HestonProcess::FullTruncation)
        .value("Reflection", HestonProcess::Reflection)
        .value("NonCentralChiSquareVariance", HestonProcess::NonCentralChiSquareVariance)
        .value("QuadraticExponential", HestonProcess::QuadraticExponential)
        .value("QuadraticExponentialMartingale", HestonProcess::QuadraticExponentialMartingale)
        .value("BroadieKayaExactSchemeLobatto", HestonProcess::BroadieKayaExactSchemeLobatto)
        .value("BroadieKayaExactSchemeLaguerre", HestonProcess::BroadieKayaExactSchemeLaguerre)
        .value("BroadieKayaExactSchemeTrapezoidal", HestonProcess::BroadieKayaExactSchemeTrapezoidal)
        .export_values();

    cls.def(py::init<Handle<YieldTermStructure>,
                     Handle<YieldTermStructure>,
                     Handle<Quote>,
                     Real, Real, Real, Real, Real,
                     HestonProcess::Discretization>(),
            py::arg("riskFreeRate"), py::arg("dividendYield"), py::arg("s0"),
            py::arg("v0"), py::arg("kappa"), py::arg("theta"),
            py::arg("sigma"), py::arg("rho"),
            py::arg("d") = HestonProcess::QuadraticExponentialMartingale)
        .def("v0", &HestonProcess::v0,
            "Returns the initial variance.")
        .def("rho", &HestonProcess::rho,
            "Returns the correlation between spot and variance.")
        .def("kappa", &HestonProcess::kappa,
            "Returns the mean-reversion speed.")
        .def("theta", &HestonProcess::theta,
            "Returns the long-term variance.")
        .def("sigma", &HestonProcess::sigma,
            "Returns the volatility of volatility.")
        .def("s0", &HestonProcess::s0,
            "Returns the initial spot price handle.")
        .def("dividendYield", &HestonProcess::dividendYield,
            "Returns the dividend yield term structure handle.")
        .def("riskFreeRate", &HestonProcess::riskFreeRate,
            "Returns the risk-free rate term structure handle.")
        .def("pdf", &HestonProcess::pdf,
            py::arg("x"), py::arg("v"), py::arg("t"), py::arg("eps") = 1e-3,
            "Returns the probability density at (x, v) for time t, where x is log-spot.");
}
