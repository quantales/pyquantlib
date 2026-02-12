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
#include <ql/termstructures/volatility/capfloor/capfloortermvolsurface.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::capfloortermvolsurface(py::module_& m) {
    // Diamond: LazyObject + CapFloorTermVolatilityStructure (both through Observable)
    py::classh<CapFloorTermVolSurface,
               LazyObject, CapFloorTermVolatilityStructure>(
        m, "CapFloorTermVolSurface",
        "Cap/floor smile volatility surface.")
        // Floating reference date, fixed market data
        .def(py::init<Natural, const Calendar&, BusinessDayConvention,
                      const std::vector<Period>&, const std::vector<Rate>&,
                      const Matrix&, const DayCounter&>(),
            py::arg("settlementDays"), py::arg("calendar"),
            py::arg("businessDayConvention"),
            py::arg("optionTenors"), py::arg("strikes"),
            py::arg("volatilities"),
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs from settlement days and volatility matrix.")
        // Fixed reference date, fixed market data
        .def(py::init<const Date&, const Calendar&, BusinessDayConvention,
                      const std::vector<Period>&, const std::vector<Rate>&,
                      const Matrix&, const DayCounter&>(),
            py::arg("settlementDate"), py::arg("calendar"),
            py::arg("businessDayConvention"),
            py::arg("optionTenors"), py::arg("strikes"),
            py::arg("volatilities"),
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs from settlement date and volatility matrix.")
        .def("optionTenors", &CapFloorTermVolSurface::optionTenors,
            py::return_value_policy::reference_internal,
            "Returns the option tenors.")
        .def("optionDates", &CapFloorTermVolSurface::optionDates,
            py::return_value_policy::reference_internal,
            "Returns the option dates.")
        .def("optionTimes", &CapFloorTermVolSurface::optionTimes,
            py::return_value_policy::reference_internal,
            "Returns the option times.")
        .def("strikes", &CapFloorTermVolSurface::strikes,
            py::return_value_policy::reference_internal,
            "Returns the strikes.")
        .def("maxDate", &CapFloorTermVolSurface::maxDate,
            "Returns the maximum date.")
        .def("minStrike", &CapFloorTermVolSurface::minStrike,
            "Returns the minimum strike.")
        .def("maxStrike", &CapFloorTermVolSurface::maxStrike,
            "Returns the maximum strike.");
}
