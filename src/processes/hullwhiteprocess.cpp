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
#include <ql/processes/hullwhiteprocess.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_processes::hullwhiteprocess(py::module_& m) {
    py::class_<HullWhiteProcess, StochasticProcess1D,
               ext::shared_ptr<HullWhiteProcess>>(
        m, "HullWhiteProcess",
        "Hull-White short-rate stochastic process.")
        .def(py::init<const Handle<YieldTermStructure>&, Real, Real>(),
            py::arg("riskFreeRate"),
            py::arg("a"),
            py::arg("sigma"),
            "Constructs from yield term structure handle.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& yts,
                         Real a, Real sigma) {
                return ext::make_shared<HullWhiteProcess>(
                    Handle<YieldTermStructure>(yts), a, sigma);
             }),
            py::arg("riskFreeRate"),
            py::arg("a"),
            py::arg("sigma"),
            "Constructs from yield term structure (handle created internally).")
        .def("a", &HullWhiteProcess::a,
            "Returns mean reversion speed.")
        .def("sigma", &HullWhiteProcess::sigma,
            "Returns volatility.")
        .def("alpha", &HullWhiteProcess::alpha,
            py::arg("t"),
            "Returns alpha at time t.");

    // HullWhiteForwardProcess (same header)
    py::class_<HullWhiteForwardProcess, ForwardMeasureProcess1D,
               ext::shared_ptr<HullWhiteForwardProcess>>(
        m, "HullWhiteForwardProcess",
        "Hull-White forward-measure short-rate process.")
        .def(py::init<const Handle<YieldTermStructure>&, Real, Real>(),
            py::arg("riskFreeRate"),
            py::arg("a"),
            py::arg("sigma"),
            "Constructs from yield term structure handle.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& yts,
                         Real a, Real sigma) {
                return ext::make_shared<HullWhiteForwardProcess>(
                    Handle<YieldTermStructure>(yts), a, sigma);
             }),
            py::arg("riskFreeRate"),
            py::arg("a"),
            py::arg("sigma"),
            "Constructs from yield term structure (handle created internally).")
        .def("a", &HullWhiteForwardProcess::a,
            "Returns mean reversion speed.")
        .def("sigma", &HullWhiteForwardProcess::sigma,
            "Returns volatility.")
        .def("alpha", &HullWhiteForwardProcess::alpha,
            py::arg("t"),
            "Returns alpha at time t.")
        .def("M_T", &HullWhiteForwardProcess::M_T,
            py::arg("s"), py::arg("t"), py::arg("T"),
            "Returns forward-measure adjustment M_T(s, t, T).")
        .def("B", &HullWhiteForwardProcess::B,
            py::arg("t"), py::arg("T"),
            "Returns discount bond function B(t, T).");
}
