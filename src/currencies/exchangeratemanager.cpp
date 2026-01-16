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
#include <ql/currencies/exchangeratemanager.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_currencies::exchangeratemanager(py::module_& m) {
    py::class_<ExchangeRateManager, std::unique_ptr<ExchangeRateManager, py::nodelete>>(
        m, "ExchangeRateManager",
        "Global repository for exchange rates.")

        .def_static("instance", &ExchangeRateManager::instance,
            py::return_value_policy::reference,
            "Returns the singleton instance.")

        .def("add", &ExchangeRateManager::add,
            py::arg("rate"),
            py::arg("startDate") = Date::minDate(),
            py::arg("endDate") = Date::maxDate(),
            "Adds an exchange rate.")

        .def("lookup", &ExchangeRateManager::lookup,
            py::arg("source"),
            py::arg("target"),
            py::arg("date") = Date(),
            py::arg("type") = ExchangeRate::Derived,
            "Looks up an exchange rate between two currencies.")

        .def("clear", &ExchangeRateManager::clear,
            "Clears all stored exchange rates.");
}
