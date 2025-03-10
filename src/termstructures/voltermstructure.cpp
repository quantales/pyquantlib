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
#include <ql/termstructures/voltermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::voltermstructure(py::module_& m) {
    py::class_<VolatilityTermStructure, PyVolatilityTermStructure,
               ext::shared_ptr<VolatilityTermStructure>, TermStructure>(
        m, "VolatilityTermStructure",
        "Abstract base class for volatility term structures.")
        .def(py::init<const Date&, const Calendar&, BusinessDayConvention,
                      const DayCounter&>(),
            py::arg("referenceDate"),
            py::arg("calendar"),
            py::arg("businessDayConvention"),
            py::arg("dayCounter"),
            "Constructs with reference date, calendar, convention, and day counter.")
        .def(py::init<Natural, const Calendar&, BusinessDayConvention,
                      const DayCounter&>(),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("businessDayConvention"),
            py::arg("dayCounter"),
            "Constructs with settlement days, calendar, convention, and day counter.")
        .def("businessDayConvention", &VolatilityTermStructure::businessDayConvention,
            "Returns the business day convention.")
        .def("optionDateFromTenor", &VolatilityTermStructure::optionDateFromTenor,
            py::arg("tenor"),
            "Returns the option date for the given tenor.")
        .def("minStrike", &VolatilityTermStructure::minStrike,
            "Returns the minimum strike for which the term structure is defined.")
        .def("maxStrike", &VolatilityTermStructure::maxStrike,
            "Returns the maximum strike for which the term structure is defined.");
}
