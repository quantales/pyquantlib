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
#include <ql/termstructures/volatility/optionlet/strippedoptionletbase.hpp>
#include <ql/time/daycounter.hpp>
#include <ql/time/calendar.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::strippedoptionletbase(py::module_& m) {
    py::class_<StrippedOptionletBase,
               ext::shared_ptr<StrippedOptionletBase>, LazyObject>(
        m, "StrippedOptionletBase",
        "Abstract base class for stripped optionlet volatility data.")
        .def("optionletStrikes", &StrippedOptionletBase::optionletStrikes,
            py::arg("i"),
            py::return_value_policy::reference_internal,
            "Returns optionlet strikes for the i-th maturity.")
        .def("optionletVolatilities", &StrippedOptionletBase::optionletVolatilities,
            py::arg("i"),
            py::return_value_policy::reference_internal,
            "Returns optionlet volatilities for the i-th maturity.")
        .def("optionletFixingDates", &StrippedOptionletBase::optionletFixingDates,
            py::return_value_policy::reference_internal,
            "Returns optionlet fixing dates.")
        .def("optionletFixingTimes", &StrippedOptionletBase::optionletFixingTimes,
            py::return_value_policy::reference_internal,
            "Returns optionlet fixing times.")
        .def("optionletMaturities", &StrippedOptionletBase::optionletMaturities,
            "Returns the number of optionlet maturities.")
        .def("atmOptionletRates", &StrippedOptionletBase::atmOptionletRates,
            py::return_value_policy::reference_internal,
            "Returns ATM optionlet rates.")
        .def("dayCounter", &StrippedOptionletBase::dayCounter,
            "Returns the day counter.")
        .def("calendar", &StrippedOptionletBase::calendar,
            "Returns the calendar.")
        .def("settlementDays", &StrippedOptionletBase::settlementDays,
            "Returns the number of settlement days.")
        .def("businessDayConvention", &StrippedOptionletBase::businessDayConvention,
            "Returns the business day convention.")
        .def("volatilityType", &StrippedOptionletBase::volatilityType,
            "Returns the volatility type.")
        .def("displacement", &StrippedOptionletBase::displacement,
            "Returns the displacement for shifted lognormal volatilities.");
}
