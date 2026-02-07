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
#include <ql/instruments/forwardrateagreement.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::forwardrateagreement(py::module_& m) {
    // Position::Type enum
    py::enum_<Position::Type>(m, "PositionType",
        "Long or short position.")
        .value("Long", Position::Long)
        .value("Short", Position::Short);

    // ForwardRateAgreement class
    py::class_<ForwardRateAgreement, Instrument,
               ext::shared_ptr<ForwardRateAgreement>>(
        m, "ForwardRateAgreement",
        "Forward rate agreement (FRA).")
        // Indexed coupon constructor
        .def(py::init<const ext::shared_ptr<IborIndex>&,
                      const Date&, Position::Type, Rate, Real,
                      Handle<YieldTermStructure>>(),
            py::arg("index"),
            py::arg("valueDate"),
            py::arg("type"),
            py::arg("strikeForwardRate"),
            py::arg("notionalAmount"),
            py::arg("discountCurve") = Handle<YieldTermStructure>(),
            "Constructs FRA using indexed coupon.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<IborIndex>& index,
                        const Date& valueDate, Position::Type type,
                        Rate strikeForwardRate, Real notionalAmount,
                        const ext::shared_ptr<YieldTermStructure>& disc) {
            return ext::make_shared<ForwardRateAgreement>(
                index, valueDate, type, strikeForwardRate, notionalAmount,
                disc ? Handle<YieldTermStructure>(disc)
                     : Handle<YieldTermStructure>());
        }),
            py::arg("index"),
            py::arg("valueDate"),
            py::arg("type"),
            py::arg("strikeForwardRate"),
            py::arg("notionalAmount"),
            py::arg("discountCurve"),
            "Constructs FRA with term structure (handle created internally).")
        // Par-rate approximation constructor
        .def(py::init<const ext::shared_ptr<IborIndex>&,
                      const Date&, const Date&, Position::Type, Rate, Real,
                      Handle<YieldTermStructure>>(),
            py::arg("index"),
            py::arg("valueDate"),
            py::arg("maturityDate"),
            py::arg("type"),
            py::arg("strikeForwardRate"),
            py::arg("notionalAmount"),
            py::arg("discountCurve") = Handle<YieldTermStructure>(),
            "Constructs FRA using par-rate approximation.")
        // Inspectors
        .def("isExpired", &ForwardRateAgreement::isExpired,
            "Returns True if expired.")
        .def("amount", &ForwardRateAgreement::amount,
            "Returns the payoff on the value date.")
        .def("calendar", &ForwardRateAgreement::calendar,
            py::return_value_policy::reference_internal,
            "Returns the calendar.")
        .def("businessDayConvention", &ForwardRateAgreement::businessDayConvention,
            "Returns the business day convention.")
        .def("dayCounter", &ForwardRateAgreement::dayCounter,
            py::return_value_policy::reference_internal,
            "Returns the day counter.")
        .def("fixingDate", &ForwardRateAgreement::fixingDate,
            "Returns the fixing date.")
        .def("forwardRate", &ForwardRateAgreement::forwardRate,
            "Returns the market forward rate.");
}
