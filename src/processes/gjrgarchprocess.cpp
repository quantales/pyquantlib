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
#include <ql/processes/gjrgarchprocess.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_processes::gjrgarchprocess(py::module_& m) {
    py::enum_<GJRGARCHProcess::Discretization>(
        m, "GJRGARCHProcessDiscretization",
        "Discretization scheme for GJR-GARCH process.")
        .value("PartialTruncation", GJRGARCHProcess::PartialTruncation)
        .value("FullTruncation", GJRGARCHProcess::FullTruncation)
        .value("Reflection", GJRGARCHProcess::Reflection);

    py::class_<GJRGARCHProcess, StochasticProcess,
               ext::shared_ptr<GJRGARCHProcess>>(
        m, "GJRGARCHProcess",
        "GJR-GARCH(1,1) stochastic process.")
        .def(py::init<Handle<YieldTermStructure>,
                      Handle<YieldTermStructure>,
                      Handle<Quote>,
                      Real, Real, Real, Real, Real, Real,
                      Real, GJRGARCHProcess::Discretization>(),
             py::arg("riskFreeRate"),
             py::arg("dividendYield"),
             py::arg("s0"),
             py::arg("v0"),
             py::arg("omega"),
             py::arg("alpha"),
             py::arg("beta"),
             py::arg("gamma"),
             py::arg("lambda_"),
             py::arg("daysPerYear") = 252.0,
             py::arg("discretization") = GJRGARCHProcess::FullTruncation)
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& riskFreeRate,
                         const ext::shared_ptr<YieldTermStructure>& dividendYield,
                         const ext::shared_ptr<Quote>& s0,
                         Real v0, Real omega, Real alpha, Real beta,
                         Real gamma, Real lambda, Real daysPerYear,
                         GJRGARCHProcess::Discretization d) {
                 return ext::make_shared<GJRGARCHProcess>(
                     Handle<YieldTermStructure>(riskFreeRate),
                     Handle<YieldTermStructure>(dividendYield),
                     Handle<Quote>(s0),
                     v0, omega, alpha, beta, gamma, lambda,
                     daysPerYear, d);
             }),
             py::arg("riskFreeRate"),
             py::arg("dividendYield"),
             py::arg("s0"),
             py::arg("v0"),
             py::arg("omega"),
             py::arg("alpha"),
             py::arg("beta"),
             py::arg("gamma"),
             py::arg("lambda_"),
             py::arg("daysPerYear") = 252.0,
             py::arg("discretization") = GJRGARCHProcess::FullTruncation,
             "Constructs from shared_ptr objects (handles created internally).")
        .def("v0", &GJRGARCHProcess::v0, "Returns initial variance.")
        .def("lambda_", [](const GJRGARCHProcess& p) { return p.lambda(); },
             "Returns market price of risk.")
        .def("omega", &GJRGARCHProcess::omega, "Returns omega.")
        .def("alpha", &GJRGARCHProcess::alpha, "Returns alpha.")
        .def("beta", &GJRGARCHProcess::beta, "Returns beta.")
        .def("gamma", &GJRGARCHProcess::gamma, "Returns gamma.")
        .def("daysPerYear", &GJRGARCHProcess::daysPerYear,
             "Returns trading days per year.")
        .def("s0", &GJRGARCHProcess::s0,
             py::return_value_policy::reference_internal,
             "Returns the spot price handle.")
        .def("dividendYield", &GJRGARCHProcess::dividendYield,
             py::return_value_policy::reference_internal,
             "Returns the dividend yield handle.")
        .def("riskFreeRate", &GJRGARCHProcess::riskFreeRate,
             py::return_value_policy::reference_internal,
             "Returns the risk-free rate handle.");
}
