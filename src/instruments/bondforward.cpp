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
#include <ql/instruments/bondforward.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::bondforward(py::module_& m) {
    py::class_<BondForward, Forward, ext::shared_ptr<BondForward>>(
        m, "BondForward",
        "Forward contract on a bond.")
        // Full constructor with Handle
        .def(py::init<const Date&, const Date&, Position::Type, Real,
                      Natural, const DayCounter&, const Calendar&,
                      BusinessDayConvention,
                      const ext::shared_ptr<Bond>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<YieldTermStructure>&>(),
            py::arg("valueDate"),
            py::arg("maturityDate"),
            py::arg("type"),
            py::arg("strike"),
            py::arg("settlementDays"),
            py::arg("dayCounter"),
            py::arg("calendar"),
            py::arg("businessDayConvention"),
            py::arg("bond"),
            py::arg("discountCurve") = Handle<YieldTermStructure>(),
            py::arg("incomeDiscountCurve") = Handle<YieldTermStructure>(),
            "Constructs a bond forward.")
        // Hidden handle constructor
        .def(py::init([](const Date& valueDate, const Date& maturityDate,
                         Position::Type type, Real strike,
                         Natural settlementDays, const DayCounter& dayCounter,
                         const Calendar& calendar,
                         BusinessDayConvention bdc,
                         const ext::shared_ptr<Bond>& bond,
                         const ext::shared_ptr<YieldTermStructure>& discountCurve,
                         const ext::shared_ptr<YieldTermStructure>& incomeDiscountCurve) {
            return ext::make_shared<BondForward>(
                valueDate, maturityDate, type, strike, settlementDays,
                dayCounter, calendar, bdc, bond,
                Handle<YieldTermStructure>(discountCurve),
                Handle<YieldTermStructure>(incomeDiscountCurve));
        }),
            py::arg("valueDate"),
            py::arg("maturityDate"),
            py::arg("type"),
            py::arg("strike"),
            py::arg("settlementDays"),
            py::arg("dayCounter"),
            py::arg("calendar"),
            py::arg("businessDayConvention"),
            py::arg("bond"),
            py::arg("discountCurve"),
            py::arg("incomeDiscountCurve"),
            "Constructs a bond forward (handles created internally).")
        // Calculations
        .def("forwardPrice", &BondForward::forwardPrice,
            "Returns the dirty forward bond price.")
        .def("cleanForwardPrice", &BondForward::cleanForwardPrice,
            "Returns the clean forward bond price.");
}
