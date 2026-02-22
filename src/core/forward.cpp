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
#include <ql/instruments/forward.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_core::forward(py::module_& m) {
    auto base = py::module_::import("pyquantlib.base");

    // Forward ABC (protected constructor, not directly instantiable)
    py::class_<Forward, Instrument, ext::shared_ptr<Forward>>(base, "Forward",
        "Abstract base class for forward contracts.")
        // Inspectors
        .def("settlementDate", &Forward::settlementDate,
            "Returns the settlement date.")
        .def("calendar", &Forward::calendar,
            py::return_value_policy::reference_internal,
            "Returns the calendar.")
        .def("businessDayConvention", &Forward::businessDayConvention,
            "Returns the business day convention.")
        .def("dayCounter", &Forward::dayCounter,
            py::return_value_policy::reference_internal,
            "Returns the day counter.")
        .def("discountCurve", &Forward::discountCurve,
            "Returns the discount curve handle.")
        .def("incomeDiscountCurve", &Forward::incomeDiscountCurve,
            "Returns the income discount curve handle.")
        .def("isExpired", &Forward::isExpired,
            "Returns True if the forward has expired.")
        // Calculations
        .def("spotValue", &Forward::spotValue,
            "Returns the spot value of the underlying.")
        .def("spotIncome", &Forward::spotIncome,
            py::arg("incomeDiscountCurve"),
            "Returns the NPV of income from the underlying.")
        .def("forwardValue", &Forward::forwardValue,
            "Returns the forward value of the underlying.")
        .def("impliedYield", &Forward::impliedYield,
            py::arg("underlyingSpotValue"),
            py::arg("forwardValue"),
            py::arg("settlementDate"),
            py::arg("compoundingConvention"),
            py::arg("dayCounter"),
            "Returns the implied yield from spot and forward values.");

    // ForwardTypePayoff
    py::class_<ForwardTypePayoff, Payoff, ext::shared_ptr<ForwardTypePayoff>>(
        m, "ForwardTypePayoff",
        "Payoff for forward contracts.")
        .def(py::init<Position::Type, Real>(),
            py::arg("type"), py::arg("strike"),
            "Constructs a forward payoff.")
        .def("forwardType", &ForwardTypePayoff::forwardType,
            "Returns the position type.")
        .def("strike", &ForwardTypePayoff::strike,
            "Returns the strike price.");
}
