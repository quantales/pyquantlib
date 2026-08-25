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
#include <ql/time/calendars/islamicholidays.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_time::islamicholidays(py::module_& m) {
    auto sub = m.def_submodule("MoonSightingMethod",
        "Islamic holiday lookups following the moon-sighting calendar.");

    sub.def("isEidAlFitr", &MoonSightingMethod::isEidAlFitr,
        py::arg("date"),
        "Returns true if the date falls on Eid al-Fitr.");
    sub.def("isEidAlAdha", &MoonSightingMethod::isEidAlAdha,
        py::arg("date"),
        "Returns true if the date falls on Eid al-Adha.");
}
