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
#include <ql/time/weekday.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_time::weekday(py::module_& m)
{
    py::enum_<QuantLib::Weekday>(m, "Weekday", py::arithmetic(),
        "Days of the week enumeration.")
    .value("Sunday", QuantLib::Sunday)
    .value("Monday", QuantLib::Monday)
    .value("Tuesday", QuantLib::Tuesday)
    .value("Wednesday", QuantLib::Wednesday)
    .value("Thursday", QuantLib::Thursday)
    .value("Friday", QuantLib::Friday)
    .value("Saturday", QuantLib::Saturday)
    .value("Sun", QuantLib::Sun)
    .value("Mon", QuantLib::Mon)
    .value("Tue", QuantLib::Tue)
    .value("Wed", QuantLib::Wed)
    .value("Thu", QuantLib::Thu)
    .value("Fri", QuantLib::Fri)
    .value("Sat", QuantLib::Sat)
    .export_values();
}