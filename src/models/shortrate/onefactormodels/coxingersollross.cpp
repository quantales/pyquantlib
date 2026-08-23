/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/models/shortrate/onefactormodels/coxingersollross.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::coxingersollross(py::module_& m) {
    py::class_<CoxIngersollRoss, OneFactorAffineModel,
               ext::shared_ptr<CoxIngersollRoss>>(
        m, "CoxIngersollRoss",
        "Cox-Ingersoll-Ross short-rate model.")
        .def(py::init<Rate, Real, Real, Real, bool>(),
            py::arg("r0") = 0.05,
            py::arg("theta") = 0.1,
            py::arg("k") = 0.1,
            py::arg("sigma") = 0.1,
            py::arg("withFellerConstraint") = true,
            "Constructs CIR model.")
        .def("discountBondOption", &CoxIngersollRoss::discountBondOption,
            py::arg("type"), py::arg("strike"),
            py::arg("maturity"), py::arg("bondMaturity"),
            "Returns discount bond option price.");
}
