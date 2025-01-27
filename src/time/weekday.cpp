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