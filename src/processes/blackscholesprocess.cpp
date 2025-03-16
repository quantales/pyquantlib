/*
 * PyQuantLib: Python bindings for QuantLib
 * Copyright (c) 2025 Yassine Idyiahia
 *
 * QuantLib is Copyright (c) 2000-2025 The QuantLib Authors
 * QuantLib is free software under a modified BSD license.
 * See http://quantlib.org/ for more information.
 *
 * Source: https://github.com/quantales/pyquantlib
 * Licensed under the BSD 3-Clause License. See LICENSE file for details.
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_processes::blackscholesprocess(py::module_& m) {
    // GeneralizedBlackScholesProcess
    py::class_<GeneralizedBlackScholesProcess, StochasticProcess1D,
               ext::shared_ptr<GeneralizedBlackScholesProcess>>(
        m, "GeneralizedBlackScholesProcess",
        "Generalized Black-Scholes-Merton stochastic process.")
        .def(py::init<const Handle<Quote>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<BlackVolTermStructure>&>(),
             py::arg("x0"), py::arg("dividendTS"),
             py::arg("riskFreeTS"), py::arg("blackVolTS"))
        .def(py::init<const Handle<Quote>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<BlackVolTermStructure>&,
                      const ext::shared_ptr<StochasticProcess1D::discretization>&>(),
             py::arg("x0"), py::arg("dividendTS"), py::arg("riskFreeTS"),
             py::arg("blackVolTS"), py::arg("discretization"))
        .def("stateVariable", &GeneralizedBlackScholesProcess::stateVariable,
            "Returns the state variable handle.")
        .def("dividendYield", &GeneralizedBlackScholesProcess::dividendYield,
            "Returns the dividend yield term structure handle.")
        .def("riskFreeRate", &GeneralizedBlackScholesProcess::riskFreeRate,
            "Returns the risk-free rate term structure handle.")
        .def("localVolatility", &GeneralizedBlackScholesProcess::localVolatility,
            "Returns the local volatility term structure handle.");

    // Alias: BlackScholesMertonProcess -> GeneralizedBlackScholesProcess
    m.attr("BlackScholesMertonProcess") = m.attr("GeneralizedBlackScholesProcess");

    // BlackScholesProcess (no dividend yield)
    py::class_<BlackScholesProcess, GeneralizedBlackScholesProcess,
               ext::shared_ptr<BlackScholesProcess>>(
        m, "BlackScholesProcess",
        "Black-Scholes process with no dividend yield.")
        .def(py::init<const Handle<Quote>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<BlackVolTermStructure>&>(),
             py::arg("x0"), py::arg("riskFreeTS"), py::arg("blackVolTS"))
        .def(py::init<const Handle<Quote>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<BlackVolTermStructure>&,
                      const ext::shared_ptr<StochasticProcess1D::discretization>&,
                      bool>(),
             py::arg("x0"), py::arg("riskFreeTS"), py::arg("blackVolTS"),
             py::arg("discretization"), py::arg("forceDiscretization") = false);

    // BlackProcess (forward price dynamics)
    py::class_<BlackProcess, GeneralizedBlackScholesProcess,
               ext::shared_ptr<BlackProcess>>(
        m, "BlackProcess",
        "Black process for forward price dynamics.")
        .def(py::init<const Handle<Quote>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<BlackVolTermStructure>&>(),
             py::arg("x0"), py::arg("riskFreeTS"), py::arg("blackVolTS"))
        .def(py::init<const Handle<Quote>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<BlackVolTermStructure>&,
                      const ext::shared_ptr<StochasticProcess1D::discretization>&,
                      bool>(),
             py::arg("x0"), py::arg("riskFreeTS"), py::arg("blackVolTS"),
             py::arg("discretization"), py::arg("forceDiscretization") = false);

    // GarmanKohlhagenProcess (FX options)
    py::class_<GarmanKohlagenProcess, GeneralizedBlackScholesProcess,
               ext::shared_ptr<GarmanKohlagenProcess>>(
        m, "GarmanKohlhagenProcess",
        "Garman-Kohlhagen process for FX options.")
        .def(py::init<const Handle<Quote>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<BlackVolTermStructure>&>(),
             py::arg("x0"), py::arg("foreignRiskFreeTS"),
             py::arg("domesticRiskFreeTS"), py::arg("blackVolTS"))
        .def(py::init<const Handle<Quote>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<BlackVolTermStructure>&,
                      const ext::shared_ptr<StochasticProcess1D::discretization>&,
                      bool>(),
             py::arg("x0"), py::arg("foreignRiskFreeTS"),
             py::arg("domesticRiskFreeTS"), py::arg("blackVolTS"),
             py::arg("discretization"), py::arg("forceDiscretization") = false);
}
