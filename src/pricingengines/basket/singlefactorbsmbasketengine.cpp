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
#include <ql/pricingengines/basket/singlefactorbsmbasketengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::singlefactorbsmbasketengine(py::module_& m) {
    py::class_<SingleFactorBsmBasketEngine, PricingEngine,
               ext::shared_ptr<SingleFactorBsmBasketEngine>>(
        m, "SingleFactorBsmBasketEngine",
        "Single-factor BSM basket option engine.")
        .def(py::init<std::vector<ext::shared_ptr<GeneralizedBlackScholesProcess>>,
                      Real>(),
            py::arg("processes"),
            py::arg("xTol") = 1e4 * QL_EPSILON,
            "Constructs engine.");
}
