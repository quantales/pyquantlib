/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
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
