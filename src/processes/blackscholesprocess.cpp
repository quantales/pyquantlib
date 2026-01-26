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
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/termstructures/volatility/equityfx/localvoltermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_processes::blackscholesprocess(py::module_& m) {
    // GeneralizedBlackScholesProcess
    py::class_<GeneralizedBlackScholesProcess, StochasticProcess1D,
               ext::shared_ptr<GeneralizedBlackScholesProcess>>(
        m, "GeneralizedBlackScholesProcess",
        "Generalized Black-Scholes-Merton stochastic process.")
        // Handle-based constructors
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
        // Hidden handle constructors
        .def(py::init([](const ext::shared_ptr<Quote>& x0,
                         const ext::shared_ptr<YieldTermStructure>& dividendTS,
                         const ext::shared_ptr<YieldTermStructure>& riskFreeTS,
                         const ext::shared_ptr<BlackVolTermStructure>& blackVolTS) {
            return ext::make_shared<GeneralizedBlackScholesProcess>(
                Handle<Quote>(x0),
                Handle<YieldTermStructure>(dividendTS),
                Handle<YieldTermStructure>(riskFreeTS),
                Handle<BlackVolTermStructure>(blackVolTS));
        }), py::arg("x0"), py::arg("dividendTS"),
            py::arg("riskFreeTS"), py::arg("blackVolTS"),
            "Constructs from term structures (handles created internally).")
        .def(py::init([](const ext::shared_ptr<Quote>& x0,
                         const ext::shared_ptr<YieldTermStructure>& dividendTS,
                         const ext::shared_ptr<YieldTermStructure>& riskFreeTS,
                         const ext::shared_ptr<BlackVolTermStructure>& blackVolTS,
                         const ext::shared_ptr<StochasticProcess1D::discretization>& d) {
            return ext::make_shared<GeneralizedBlackScholesProcess>(
                Handle<Quote>(x0),
                Handle<YieldTermStructure>(dividendTS),
                Handle<YieldTermStructure>(riskFreeTS),
                Handle<BlackVolTermStructure>(blackVolTS), d);
        }), py::arg("x0"), py::arg("dividendTS"), py::arg("riskFreeTS"),
            py::arg("blackVolTS"), py::arg("discretization"),
            "Constructs from term structures with discretization (handles created internally).")
        // Handle-based constructor with external local vol
        .def(py::init<const Handle<Quote>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<BlackVolTermStructure>&,
                      const Handle<LocalVolTermStructure>&>(),
             py::arg("x0"), py::arg("dividendTS"), py::arg("riskFreeTS"),
             py::arg("blackVolTS"), py::arg("localVolTS"))
        // Hidden handle constructor with external local vol
        .def(py::init([](const ext::shared_ptr<Quote>& x0,
                         const ext::shared_ptr<YieldTermStructure>& dividendTS,
                         const ext::shared_ptr<YieldTermStructure>& riskFreeTS,
                         const ext::shared_ptr<BlackVolTermStructure>& blackVolTS,
                         const ext::shared_ptr<LocalVolTermStructure>& localVolTS) {
            return ext::make_shared<GeneralizedBlackScholesProcess>(
                Handle<Quote>(x0),
                Handle<YieldTermStructure>(dividendTS),
                Handle<YieldTermStructure>(riskFreeTS),
                Handle<BlackVolTermStructure>(blackVolTS),
                Handle<LocalVolTermStructure>(localVolTS));
        }), py::arg("x0"), py::arg("dividendTS"), py::arg("riskFreeTS"),
            py::arg("blackVolTS"), py::arg("localVolTS"),
            "Constructs with external local vol (handles created internally).")
        .def("stateVariable", &GeneralizedBlackScholesProcess::stateVariable,
            "Returns the state variable handle.")
        .def("dividendYield", &GeneralizedBlackScholesProcess::dividendYield,
            "Returns the dividend yield term structure handle.")
        .def("riskFreeRate", &GeneralizedBlackScholesProcess::riskFreeRate,
            "Returns the risk-free rate term structure handle.")
        .def("blackVolatility", &GeneralizedBlackScholesProcess::blackVolatility,
            "Returns the Black volatility term structure handle.")
        .def("localVolatility", &GeneralizedBlackScholesProcess::localVolatility,
            "Returns the local volatility term structure handle.");

    // Alias: BlackScholesMertonProcess -> GeneralizedBlackScholesProcess
    m.attr("BlackScholesMertonProcess") = m.attr("GeneralizedBlackScholesProcess");

    // BlackScholesProcess (no dividend yield)
    py::class_<BlackScholesProcess, GeneralizedBlackScholesProcess,
               ext::shared_ptr<BlackScholesProcess>>(
        m, "BlackScholesProcess",
        "Black-Scholes process with no dividend yield.")
        // Handle-based constructors
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
             py::arg("discretization"), py::arg("forceDiscretization") = false)
        // Hidden handle constructors
        .def(py::init([](const ext::shared_ptr<Quote>& x0,
                         const ext::shared_ptr<YieldTermStructure>& riskFreeTS,
                         const ext::shared_ptr<BlackVolTermStructure>& blackVolTS) {
            return ext::make_shared<BlackScholesProcess>(
                Handle<Quote>(x0),
                Handle<YieldTermStructure>(riskFreeTS),
                Handle<BlackVolTermStructure>(blackVolTS));
        }), py::arg("x0"), py::arg("riskFreeTS"), py::arg("blackVolTS"),
            "Constructs from term structures (handles created internally).")
        .def(py::init([](const ext::shared_ptr<Quote>& x0,
                         const ext::shared_ptr<YieldTermStructure>& riskFreeTS,
                         const ext::shared_ptr<BlackVolTermStructure>& blackVolTS,
                         const ext::shared_ptr<StochasticProcess1D::discretization>& d,
                         bool forceDiscretization) {
            return ext::make_shared<BlackScholesProcess>(
                Handle<Quote>(x0),
                Handle<YieldTermStructure>(riskFreeTS),
                Handle<BlackVolTermStructure>(blackVolTS), d, forceDiscretization);
        }), py::arg("x0"), py::arg("riskFreeTS"), py::arg("blackVolTS"),
            py::arg("discretization"), py::arg("forceDiscretization") = false,
            "Constructs from term structures with discretization (handles created internally).");

    // BlackProcess (forward price dynamics)
    py::class_<BlackProcess, GeneralizedBlackScholesProcess,
               ext::shared_ptr<BlackProcess>>(
        m, "BlackProcess",
        "Black process for forward price dynamics.")
        // Handle-based constructors
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
             py::arg("discretization"), py::arg("forceDiscretization") = false)
        // Hidden handle constructors
        .def(py::init([](const ext::shared_ptr<Quote>& x0,
                         const ext::shared_ptr<YieldTermStructure>& riskFreeTS,
                         const ext::shared_ptr<BlackVolTermStructure>& blackVolTS) {
            return ext::make_shared<BlackProcess>(
                Handle<Quote>(x0),
                Handle<YieldTermStructure>(riskFreeTS),
                Handle<BlackVolTermStructure>(blackVolTS));
        }), py::arg("x0"), py::arg("riskFreeTS"), py::arg("blackVolTS"),
            "Constructs from term structures (handles created internally).")
        .def(py::init([](const ext::shared_ptr<Quote>& x0,
                         const ext::shared_ptr<YieldTermStructure>& riskFreeTS,
                         const ext::shared_ptr<BlackVolTermStructure>& blackVolTS,
                         const ext::shared_ptr<StochasticProcess1D::discretization>& d,
                         bool forceDiscretization) {
            return ext::make_shared<BlackProcess>(
                Handle<Quote>(x0),
                Handle<YieldTermStructure>(riskFreeTS),
                Handle<BlackVolTermStructure>(blackVolTS), d, forceDiscretization);
        }), py::arg("x0"), py::arg("riskFreeTS"), py::arg("blackVolTS"),
            py::arg("discretization"), py::arg("forceDiscretization") = false,
            "Constructs from term structures with discretization (handles created internally).");

    // GarmanKohlhagenProcess (FX options)
    py::class_<GarmanKohlagenProcess, GeneralizedBlackScholesProcess,
               ext::shared_ptr<GarmanKohlagenProcess>>(
        m, "GarmanKohlhagenProcess",
        "Garman-Kohlhagen process for FX options.")
        // Handle-based constructors
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
             py::arg("discretization"), py::arg("forceDiscretization") = false)
        // Hidden handle constructors
        .def(py::init([](const ext::shared_ptr<Quote>& x0,
                         const ext::shared_ptr<YieldTermStructure>& foreignRiskFreeTS,
                         const ext::shared_ptr<YieldTermStructure>& domesticRiskFreeTS,
                         const ext::shared_ptr<BlackVolTermStructure>& blackVolTS) {
            return ext::make_shared<GarmanKohlagenProcess>(
                Handle<Quote>(x0),
                Handle<YieldTermStructure>(foreignRiskFreeTS),
                Handle<YieldTermStructure>(domesticRiskFreeTS),
                Handle<BlackVolTermStructure>(blackVolTS));
        }), py::arg("x0"), py::arg("foreignRiskFreeTS"),
            py::arg("domesticRiskFreeTS"), py::arg("blackVolTS"),
            "Constructs from term structures (handles created internally).")
        .def(py::init([](const ext::shared_ptr<Quote>& x0,
                         const ext::shared_ptr<YieldTermStructure>& foreignRiskFreeTS,
                         const ext::shared_ptr<YieldTermStructure>& domesticRiskFreeTS,
                         const ext::shared_ptr<BlackVolTermStructure>& blackVolTS,
                         const ext::shared_ptr<StochasticProcess1D::discretization>& d,
                         bool forceDiscretization) {
            return ext::make_shared<GarmanKohlagenProcess>(
                Handle<Quote>(x0),
                Handle<YieldTermStructure>(foreignRiskFreeTS),
                Handle<YieldTermStructure>(domesticRiskFreeTS),
                Handle<BlackVolTermStructure>(blackVolTS), d, forceDiscretization);
        }), py::arg("x0"), py::arg("foreignRiskFreeTS"),
            py::arg("domesticRiskFreeTS"), py::arg("blackVolTS"),
            py::arg("discretization"), py::arg("forceDiscretization") = false,
            "Constructs from term structures with discretization (handles created internally).");
}
