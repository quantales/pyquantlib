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
#include <ql/pricingengines/basket/bjerksundstenslandspreadengine.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::bjerksundstenslandspreadengine(py::module_& m) {
    py::class_<BjerksundStenslandSpreadEngine, ext::shared_ptr<BjerksundStenslandSpreadEngine>,
               SpreadBlackScholesVanillaEngine>(
        m, "BjerksundStenslandSpreadEngine",
        "Bjerksund-Stensland analytical approximation for spread options.")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      Real>(),
            py::arg("process1"), py::arg("process2"), py::arg("correlation"),
            "Constructs with two Black-Scholes processes and correlation.");
}
