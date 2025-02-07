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
#include <ql/money.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <sstream>

namespace py = pybind11;
using namespace QuantLib;

void ql_core::money(py::module_& m) {
    auto pyMoney = py::class_<Money>(m, "Money",
        "Amount of cash in a specific currency.");

    // ConversionType enum
    py::enum_<Money::ConversionType>(pyMoney, "ConversionType", py::arithmetic(),
        "Conversion type for money arithmetic.")
        .value("NoConversion", Money::NoConversion,
            "Do not perform conversions.")
        .value("BaseCurrencyConversion", Money::BaseCurrencyConversion,
            "Convert both operands to base currency.")
        .value("AutomatedConversion", Money::AutomatedConversion,
            "Return result in the currency of the first operand.")
        .export_values();

    // Money::Settings singleton
    py::class_<Money::Settings, std::unique_ptr<Money::Settings, py::nodelete>>(
        pyMoney, "Settings", "Per-session settings for Money arithmetic.")
        .def_static("instance", &Money::Settings::instance,
            py::return_value_policy::reference,
            "Returns the singleton instance.")
        .def_property("conversionType",
            [](const Money::Settings& s) { return s.conversionType(); },
            [](Money::Settings& s, Money::ConversionType t) { s.conversionType() = t; },
            "The conversion type used for money arithmetic.")
        .def_property("baseCurrency",
            [](const Money::Settings& s) { return s.baseCurrency(); },
            [](Money::Settings& s, const Currency& c) { s.baseCurrency() = c; },
            "The base currency used for conversions.");

    // Money class
    pyMoney
        .def(py::init<>(),
            "Default constructor.")
        .def(py::init<Currency, Decimal>(),
            py::arg("currency"), py::arg("value"),
            "Constructs from currency and value.")
        .def(py::init<Decimal, Currency>(),
            py::arg("value"), py::arg("currency"),
            "Constructs from value and currency.")
        .def("currency", &Money::currency,
            "Returns the currency.")
        .def("value", &Money::value,
            "Returns the amount.")
        .def("rounded", &Money::rounded,
            "Returns the amount rounded according to the currency.")
        .def("__pos__", &Money::operator+)
        .def("__neg__", &Money::operator-)
        .def("__iadd__", &Money::operator+=, py::arg("other"))
        .def("__isub__", &Money::operator-=, py::arg("other"))
        .def("__imul__", &Money::operator*=, py::arg("factor"))
        .def("__itruediv__", &Money::operator/=, py::arg("divisor"))
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def(py::self < py::self)
        .def(py::self <= py::self)
        .def(py::self > py::self)
        .def(py::self >= py::self)
        .def("__str__", [](const Money& m) {
            std::ostringstream oss;
            oss << m;
            return oss.str();
        })
        .def("__repr__", [](const Money& m) {
            std::ostringstream oss;
            oss << "<Money: " << m << ">";
            return oss.str();
        });

    m.def("close",
        [](const Money& m1, const Money& m2, Size n) {
            return close(m1, m2, n);
        },
        py::arg("m1"), py::arg("m2"), py::arg("n") = 42,
        "Returns true if the two amounts are close.");

    m.def("close_enough",
        [](const Money& m1, const Money& m2, Size n) {
            return close_enough(m1, m2, n);
        },
        py::arg("m1"), py::arg("m2"), py::arg("n") = 42,
        "Returns true if the two amounts are close enough.");
}
