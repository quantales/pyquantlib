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
#include <ql/processes/merton76process.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/termstructures/volatility/equityfx/blackvoltermstructure.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_processes::merton76process(py::module_& m) {
    py::class_<Merton76Process, StochasticProcess1D,
               ext::shared_ptr<Merton76Process>>(
        m, "Merton76Process",
        "Merton jump-diffusion process.")
        // Handle constructor
        .def(py::init<const Handle<Quote>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<BlackVolTermStructure>&,
                      Handle<Quote>,
                      Handle<Quote>,
                      Handle<Quote>>(),
            py::arg("stateVariable"),
            py::arg("dividendTS"),
            py::arg("riskFreeTS"),
            py::arg("blackVolTS"),
            py::arg("jumpIntensity"),
            py::arg("logMeanJump"),
            py::arg("logJumpVolatility"),
            "Constructs from handles.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<Quote>& spot,
                         const ext::shared_ptr<YieldTermStructure>& div,
                         const ext::shared_ptr<YieldTermStructure>& rf,
                         const ext::shared_ptr<BlackVolTermStructure>& vol,
                         const ext::shared_ptr<Quote>& jumpInt,
                         const ext::shared_ptr<Quote>& logJMean,
                         const ext::shared_ptr<Quote>& logJVol) {
            return ext::make_shared<Merton76Process>(
                Handle<Quote>(spot),
                Handle<YieldTermStructure>(div),
                Handle<YieldTermStructure>(rf),
                Handle<BlackVolTermStructure>(vol),
                Handle<Quote>(jumpInt),
                Handle<Quote>(logJMean),
                Handle<Quote>(logJVol));
        }),
            py::arg("stateVariable"),
            py::arg("dividendTS"),
            py::arg("riskFreeTS"),
            py::arg("blackVolTS"),
            py::arg("jumpIntensity"),
            py::arg("logMeanJump"),
            py::arg("logJumpVolatility"),
            "Constructs from shared_ptrs (handles created internally).")
        .def("x0", &Merton76Process::x0,
            "Returns initial value.")
        .def("stateVariable", &Merton76Process::stateVariable,
            "Returns spot quote handle.")
        .def("dividendYield", &Merton76Process::dividendYield,
            "Returns dividend yield handle.")
        .def("riskFreeRate", &Merton76Process::riskFreeRate,
            "Returns risk-free rate handle.")
        .def("blackVolatility", &Merton76Process::blackVolatility,
            "Returns Black volatility handle.")
        .def("jumpIntensity", &Merton76Process::jumpIntensity,
            "Returns jump intensity handle.")
        .def("logMeanJump", &Merton76Process::logMeanJump,
            "Returns log-mean jump handle.")
        .def("logJumpVolatility", &Merton76Process::logJumpVolatility,
            "Returns log jump volatility handle.");
}
