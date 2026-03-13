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
#include <ql/pricingengines/basket/choibasketengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/math/matrix.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::choibasketengine(py::module_& m) {
    py::class_<ChoiBasketEngine, PricingEngine,
               ext::shared_ptr<ChoiBasketEngine>>(
        m, "ChoiBasketEngine",
        "Choi (2018) N-dimensional basket option engine.")
        .def(py::init<std::vector<ext::shared_ptr<GeneralizedBlackScholesProcess>>,
                      Matrix, Real, Size, bool, bool>(),
            py::arg("processes"),
            py::arg("rho"),
            py::arg("lambda") = 10.0,
            py::arg("maxNrIntegrationSteps") = std::numeric_limits<Size>::max(),
            py::arg("calcfwdDelta") = false,
            py::arg("controlVariate") = false,
            "Constructs engine.");
}
