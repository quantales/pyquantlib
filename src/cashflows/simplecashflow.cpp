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
#include <ql/cashflows/simplecashflow.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::simplecashflow(py::module_& m) {
    py::class_<SimpleCashFlow, CashFlow, ext::shared_ptr<SimpleCashFlow>>(m, "SimpleCashFlow",
        "Simple cash flow paying a fixed amount on a given date.")
        .def(py::init<Real, const Date&>(),
            py::arg("amount"), py::arg("date"),
            "Constructs a cash flow with the given amount and date.");

    py::class_<Redemption, SimpleCashFlow, ext::shared_ptr<Redemption>>(m, "Redemption",
        "Bond redemption payment.")
        .def(py::init<Real, const Date&>(),
            py::arg("amount"), py::arg("date"),
            "Constructs a redemption with the given amount and date.");

    py::class_<AmortizingPayment, SimpleCashFlow, ext::shared_ptr<AmortizingPayment>>(m, "AmortizingPayment",
        "Amortizing payment cash flow.")
        .def(py::init<Real, const Date&>(),
            py::arg("amount"), py::arg("date"),
            "Constructs an amortizing payment with the given amount and date.");
}
