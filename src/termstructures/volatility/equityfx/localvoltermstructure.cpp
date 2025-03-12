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
#include <ql/termstructures/volatility/equityfx/localvoltermstructure.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::localvoltermstructure(py::module_& m) {
    py::class_<LocalVolTermStructure, PyLocalVolTermStructure,
               ext::shared_ptr<LocalVolTermStructure>, VolatilityTermStructure>(
        m, "LocalVolTermStructure",
        "Abstract base class for local volatility term structures.")
        // Business day convention + day counter
        .def(py::init<BusinessDayConvention, const DayCounter&>(),
            py::arg("businessDayConvention") = Following,
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs with business day convention and day counter.")
        // Reference date + calendar + bdc + day counter
        .def(py::init<const Date&, const Calendar&, BusinessDayConvention,
                      const DayCounter&>(),
            py::arg("referenceDate"),
            py::arg("calendar") = Calendar(),
            py::arg("businessDayConvention") = Following,
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs with reference date.")
        // Settlement days + calendar + bdc + day counter
        .def(py::init<Natural, const Calendar&, BusinessDayConvention,
                      const DayCounter&>(),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("businessDayConvention") = Following,
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs with settlement days.")
        // Local volatility by date
        .def("localVol",
            py::overload_cast<const Date&, Real, bool>(
                &LocalVolTermStructure::localVol, py::const_),
            py::arg("date"), py::arg("underlyingLevel"),
            py::arg("extrapolate") = false,
            "Returns the local volatility for the given date and underlying level.")
        // Local volatility by time
        .def("localVol",
            py::overload_cast<Time, Real, bool>(
                &LocalVolTermStructure::localVol, py::const_),
            py::arg("time"), py::arg("underlyingLevel"),
            py::arg("extrapolate") = false,
            "Returns the local volatility for the given time and underlying level.");
}

void ql_termstructures::localvoltermstructurehandle(py::module_& m) {
    bindHandle<LocalVolTermStructure>(m, "LocalVolTermStructureHandle",
        "Handle to LocalVolTermStructure.");
}

void ql_termstructures::relinkablelocalvoltermstructurehandle(py::module_& m) {
    bindRelinkableHandle<LocalVolTermStructure>(m, "RelinkableLocalVolTermStructureHandle",
        "Relinkable handle to LocalVolTermStructure.");
}
