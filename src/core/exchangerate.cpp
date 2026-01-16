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
#include <ql/exchangerate.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_core::exchangerate(py::module_& m) {
    auto pyExchangeRate = py::class_<ExchangeRate>(m, "ExchangeRate",
        "Exchange rate between two currencies.");

    py::enum_<ExchangeRate::Type>(pyExchangeRate, "Type",
        "Type of exchange rate.")
        .value("Direct", ExchangeRate::Type::Direct,
            "Directly quoted rate.")
        .value("Derived", ExchangeRate::Type::Derived,
            "Rate derived from other rates.")
        .export_values();

    pyExchangeRate
        .def(py::init<const Currency&, const Currency&, Decimal>(),
            py::arg("source"), py::arg("target"), py::arg("rate"),
            "Constructs an exchange rate from source to target currency.")
        .def("source", &ExchangeRate::source,
            "Returns the source currency.")
        .def("target", &ExchangeRate::target,
            "Returns the target currency.")
        .def("rate", &ExchangeRate::rate,
            "Returns the exchange rate value.")
        .def("type", &ExchangeRate::type,
            "Returns the type of the exchange rate.")
        .def_static("chain", 
            static_cast<ExchangeRate (*)(const ExchangeRate&, const ExchangeRate&)>(
                &ExchangeRate::chain),
            py::arg("r1"), py::arg("r2"),
            "Creates a derived rate by chaining two rates.");
}
