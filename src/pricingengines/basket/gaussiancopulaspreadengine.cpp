/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2026 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/pricingengines/basket/gaussiancopulaspreadengine.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::gaussiancopulaspreadengine(py::module_& m) {
    py::class_<GaussianCopulaSpreadEngine,
               ext::shared_ptr<GaussianCopulaSpreadEngine>,
               BasketOption::engine>(
        m, "GaussianCopulaSpreadEngine",
        "Spread option engine using nested Gauss-Hermite quadrature over a "
        "Gaussian copula with smile-implied marginals.")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      Real, Size>(),
            py::arg("process1"), py::arg("process2"), py::arg("correlation"),
            py::arg("nPoints") = 64,
            "Constructs with two Black-Scholes processes, their correlation, "
            "and the number of quadrature points per dimension.");
}
