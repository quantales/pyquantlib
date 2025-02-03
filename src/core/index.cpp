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
#include "pyquantlib/trampolines.h"
#include <ql/index.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_core::index(py::module_& m) {
    py::class_<Index, PyIndex, ext::shared_ptr<Index>, Observable>(m, "Index",
        "Abstract base class for market indexes.")
        .def(py::init_alias<>())
        .def("name", &Index::name,
            "Returns the name of the index.")
        .def("fixingCalendar", &Index::fixingCalendar,
            "Returns the calendar used for fixing dates.")
        .def("isValidFixingDate", &Index::isValidFixingDate,
            py::arg("fixingDate"),
            "Returns true if the fixing date is valid.")
        .def("fixing", &Index::fixing,
            py::arg("fixingDate"), py::arg("forecastTodaysFixing") = false,
            "Returns the fixing for the given date.")
        .def("addFixing", &Index::addFixing,
            py::arg("fixingDate"), py::arg("fixing"), py::arg("forceOverwrite") = false,
            "Stores a fixing for the given date.")
        .def("clearFixings", &Index::clearFixings,
            "Clears all stored fixings.");
}
