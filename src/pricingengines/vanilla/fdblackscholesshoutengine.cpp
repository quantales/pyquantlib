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
#include <ql/pricingengines/vanilla/fdblackscholesshoutengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::fdblackscholesshoutengine(py::module_& m) {
    py::class_<FdBlackScholesShoutEngine,
               ext::shared_ptr<FdBlackScholesShoutEngine>,
               PricingEngine>(
        m, "FdBlackScholesShoutEngine",
        "Finite-differences Black-Scholes shout option engine.")
        // Basic constructor
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      Size, Size, Size,
                      const FdmSchemeDesc&>(),
            py::arg("process"),
            py::arg("tGrid") = 100,
            py::arg("xGrid") = 100,
            py::arg("dampingSteps") = 0,
            py::arg("schemeDesc") = FdmSchemeDesc::Douglas(),
            "Constructs FD Black-Scholes shout engine.")
        // With dividends
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      DividendSchedule,
                      Size, Size, Size,
                      const FdmSchemeDesc&>(),
            py::arg("process"),
            py::arg("dividends"),
            py::arg("tGrid") = 100,
            py::arg("xGrid") = 100,
            py::arg("dampingSteps") = 0,
            py::arg("schemeDesc") = FdmSchemeDesc::Douglas(),
            "Constructs FD Black-Scholes shout engine with dividends.");
}
