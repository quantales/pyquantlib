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
#include <ql/indexes/interestrateindex.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_indexes::interestrateindex(py::module_& m) {
    py::class_<InterestRateIndex, PyInterestRateIndex, ext::shared_ptr<InterestRateIndex>, Index>(
        m, "InterestRateIndex", "Base class for interest rate indexes.")
        .def(py::init<std::string, const Period&, Natural, Currency, Calendar, DayCounter>(),
            py::arg("familyName"),
            py::arg("tenor"),
            py::arg("fixingDays"),
            py::arg("currency"),
            py::arg("fixingCalendar"),
            py::arg("dayCounter"))
        .def("familyName", &InterestRateIndex::familyName,
            "Returns the family name.")
        .def("tenor", &InterestRateIndex::tenor,
            "Returns the tenor.")
        .def("fixingDays", &InterestRateIndex::fixingDays,
            "Returns the number of fixing days.")
        .def("currency", &InterestRateIndex::currency,
            "Returns the currency.")
        .def("dayCounter", &InterestRateIndex::dayCounter,
            "Returns the day counter.")
        .def("name", &InterestRateIndex::name,
            "Returns the index name.")
        .def("fixingCalendar", &InterestRateIndex::fixingCalendar,
            "Returns the fixing calendar.")
        .def("isValidFixingDate", &InterestRateIndex::isValidFixingDate,
            py::arg("fixingDate"),
            "Returns true if the fixing date is valid.")
        .def("fixing", &InterestRateIndex::fixing,
            py::arg("fixingDate"), py::arg("forecastTodaysFixing") = false,
            "Returns the fixing for the given date.")
        .def("fixingDate", &InterestRateIndex::fixingDate,
            py::arg("valueDate"),
            "Returns the fixing date for the given value date.")
        .def("valueDate", &InterestRateIndex::valueDate,
            py::arg("fixingDate"),
            "Returns the value date for the given fixing date.")
        .def("maturityDate", &InterestRateIndex::maturityDate,
            py::arg("valueDate"),
            "Returns the maturity date for the given value date.")
        .def("forecastFixing", &InterestRateIndex::forecastFixing,
            py::arg("fixingDate"),
            "Returns the forecasted fixing for the given date.");
}
