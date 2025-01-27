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
#include <ql/time/timeunit.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_time::timeunit(py::module_& m)
{
    py::enum_<QuantLib::TimeUnit>(m, "TimeUnit",
        "Units used to describe time periods.")
    .value("Days", QuantLib::Days)
    .value("Weeks", QuantLib::Weeks)
    .value("Months", QuantLib::Months)
    .value("Years", QuantLib::Years)
    .value("Hours", QuantLib::Hours)
    .value("Minutes", QuantLib::Minutes)
    .value("Seconds", QuantLib::Seconds)
    .value("Milliseconds", QuantLib::Milliseconds)
    .value("Microseconds", QuantLib::Microseconds)
    .export_values();
}
