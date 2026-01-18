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
#include <ql/pricingengines/basket/fd2dblackscholesvanillaengine.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::fd2dblackscholesvanillaengine(py::module_& m) {
    py::class_<Fd2dBlackScholesVanillaEngine, ext::shared_ptr<Fd2dBlackScholesVanillaEngine>,
               BasketOption::engine>(
        m, "Fd2dBlackScholesVanillaEngine",
        "2D finite-difference Black-Scholes engine for basket options.")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      Real, Size, Size, Size, Size, FdmSchemeDesc, bool, Real>(),
            py::arg("process1"), py::arg("process2"), py::arg("correlation"),
            py::arg("xGrid") = 100, py::arg("yGrid") = 100,
            py::arg("tGrid") = 50, py::arg("dampingSteps") = 0,
            py::arg("schemeDesc") = FdmSchemeDesc::Hundsdorfer(),
            py::arg("localVol") = false,
            py::arg("illegalLocalVolOverwrite") = -Null<Real>(),
            "Constructs with two processes, correlation, and optional grid/scheme parameters.");
}
