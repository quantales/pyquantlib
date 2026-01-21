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
#include <ql/models/shortrate/onefactormodel.hpp>
#include <ql/models/shortrate/onefactormodels/vasicek.hpp>
#include <ql/option.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::vasicek(py::module_& m) {
    py::class_<Vasicek, OneFactorAffineModel, ext::shared_ptr<Vasicek>>(
        m, "Vasicek",
        "Vasicek short-rate model: dr = a(b - r)dt + sigma*dW.")
        .def(py::init<Rate, Real, Real, Real, Real>(),
            py::arg("r0") = 0.05,
            py::arg("a") = 0.1,
            py::arg("b") = 0.05,
            py::arg("sigma") = 0.01,
            py::arg("lambda") = 0.0,
            "Constructs Vasicek model with initial rate, mean reversion, "
            "long-term rate, volatility, and risk premium.")
        .def("r0", &Vasicek::r0, "Returns initial short rate.")
        .def("a", &Vasicek::a, "Returns mean reversion speed.")
        .def("b", &Vasicek::b, "Returns long-term mean rate.")
        .def("sigma", &Vasicek::sigma, "Returns volatility.")
        .def_property_readonly("lambda_", &Vasicek::lambda, "Returns risk premium.")
        .def("discountBondOption",
            py::overload_cast<Option::Type, Real, Time, Time>(
                &Vasicek::discountBondOption, py::const_),
            py::arg("type"), py::arg("strike"), py::arg("maturity"), py::arg("bondMaturity"),
            "Returns discount bond option price.");
}
