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
#include <ql/quantlib.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_time::frequency(py::module_& m)
{
    py::enum_<QuantLib::Frequency>(m, "Frequency", py::arithmetic(),
        "Frequency of events.")
    .value("NoFrequency", QuantLib::NoFrequency, "Null frequency")
    .value("Once", QuantLib::Once, "Only once, e.g., a zero-coupon")
    .value("Annual", QuantLib::Annual, "Once a year")
    .value("Semiannual", QuantLib::Semiannual, "Twice a year")
    .value("EveryFourthMonth", QuantLib::EveryFourthMonth, "Every fourth month")
    .value("Quarterly", QuantLib::Quarterly, "Every third month")
    .value("Bimonthly", QuantLib::Bimonthly, "Every second month")
    .value("Monthly", QuantLib::Monthly, "Once a month")
    .value("EveryFourthWeek", QuantLib::EveryFourthWeek, "Every fourth week")
    .value("Biweekly", QuantLib::Biweekly, "Every second week")
    .value("Weekly", QuantLib::Weekly, "Once a week")
    .value("Daily", QuantLib::Daily, "Once a day")
    .value("OtherFrequency", QuantLib::OtherFrequency, "Some other unknown frequency")
    .export_values();
}