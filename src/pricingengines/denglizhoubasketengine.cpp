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
#include <ql/pricingengines/basket/denglizhoubasketengine.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::denglizhoubasketengine(py::module_& m) {
    py::class_<DengLiZhouBasketEngine, ext::shared_ptr<DengLiZhouBasketEngine>,
               BasketOption::engine>(
        m, "DengLiZhouBasketEngine",
        "Deng-Li-Zhou analytical approximation for N-dim basket options.")
        .def(py::init<std::vector<ext::shared_ptr<GeneralizedBlackScholesProcess>>,
                      Matrix>(),
            py::arg("processes"), py::arg("correlation"),
            "Constructs with vector of Black-Scholes processes and correlation matrix.");
}
