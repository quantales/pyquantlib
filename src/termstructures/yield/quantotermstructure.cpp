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
#include <ql/termstructures/yield/quantotermstructure.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/termstructures/volatility/equityfx/blackvoltermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::quantotermstructure(py::module_& m) {
    py::class_<QuantoTermStructure, YieldTermStructure,
               ext::shared_ptr<QuantoTermStructure>>(
        m, "QuantoTermStructure",
        "Quanto-adjusted dividend yield term structure.")
        // Handle constructor
        .def(py::init<const Handle<YieldTermStructure>&,
                      Handle<YieldTermStructure>,
                      Handle<YieldTermStructure>,
                      Handle<BlackVolTermStructure>,
                      Real,
                      Handle<BlackVolTermStructure>,
                      Real, Real>(),
            py::arg("underlyingDividendTS"),
            py::arg("riskFreeTS"),
            py::arg("foreignRiskFreeTS"),
            py::arg("underlyingBlackVolTS"),
            py::arg("strike"),
            py::arg("exchRateBlackVolTS"),
            py::arg("exchRateATMlevel"),
            py::arg("underlyingExchRateCorrelation"),
            "Constructs from handles.")
        // Hidden handle
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& divTS,
                         const ext::shared_ptr<YieldTermStructure>& rfTS,
                         const ext::shared_ptr<YieldTermStructure>& fxTS,
                         const ext::shared_ptr<BlackVolTermStructure>& volTS,
                         Real strike,
                         const ext::shared_ptr<BlackVolTermStructure>& fxVolTS,
                         Real fxATM, Real corr) {
            return ext::make_shared<QuantoTermStructure>(
                Handle<YieldTermStructure>(divTS),
                Handle<YieldTermStructure>(rfTS),
                Handle<YieldTermStructure>(fxTS),
                Handle<BlackVolTermStructure>(volTS),
                strike,
                Handle<BlackVolTermStructure>(fxVolTS),
                fxATM, corr);
        }),
            py::arg("underlyingDividendTS"),
            py::arg("riskFreeTS"),
            py::arg("foreignRiskFreeTS"),
            py::arg("underlyingBlackVolTS"),
            py::arg("strike"),
            py::arg("exchRateBlackVolTS"),
            py::arg("exchRateATMlevel"),
            py::arg("underlyingExchRateCorrelation"),
            "Constructs from shared_ptrs (handles created internally).");
}
