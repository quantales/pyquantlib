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
#include <ql/experimental/variancegamma/variancegammaprocess.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_experimental::variancegammaprocess(py::module_& m) {
    py::class_<VarianceGammaProcess, StochasticProcess1D,
               ext::shared_ptr<VarianceGammaProcess>>(
        m, "VarianceGammaProcess",
        "Variance Gamma stochastic process.")
        .def(py::init<Handle<Quote>,
                      Handle<YieldTermStructure>,
                      Handle<YieldTermStructure>,
                      Real, Real, Real>(),
             py::arg("s0"),
             py::arg("dividendYield"),
             py::arg("riskFreeRate"),
             py::arg("sigma"),
             py::arg("nu"),
             py::arg("theta"))
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<Quote>& s0,
                         const ext::shared_ptr<YieldTermStructure>& dividendYield,
                         const ext::shared_ptr<YieldTermStructure>& riskFreeRate,
                         Real sigma, Real nu, Real theta) {
                 return ext::make_shared<VarianceGammaProcess>(
                     Handle<Quote>(s0),
                     Handle<YieldTermStructure>(dividendYield),
                     Handle<YieldTermStructure>(riskFreeRate),
                     sigma, nu, theta);
             }),
             py::arg("s0"),
             py::arg("dividendYield"),
             py::arg("riskFreeRate"),
             py::arg("sigma"),
             py::arg("nu"),
             py::arg("theta"),
             "Constructs from shared_ptr objects (handles created internally).")
        .def("sigma", &VarianceGammaProcess::sigma,
             "Returns sigma (volatility of the Brownian motion).")
        .def("nu", &VarianceGammaProcess::nu,
             "Returns nu (variance rate of the gamma process).")
        .def("theta", &VarianceGammaProcess::theta,
             "Returns theta (drift of the Brownian motion).")
        .def("s0", &VarianceGammaProcess::s0,
             py::return_value_policy::reference_internal,
             "Returns the spot price handle.")
        .def("dividendYield", &VarianceGammaProcess::dividendYield,
             py::return_value_policy::reference_internal,
             "Returns the dividend yield handle.")
        .def("riskFreeRate", &VarianceGammaProcess::riskFreeRate,
             py::return_value_policy::reference_internal,
             "Returns the risk-free rate handle.");
}
