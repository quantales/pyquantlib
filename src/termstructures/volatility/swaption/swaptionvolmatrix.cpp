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
#include <ql/termstructures/volatility/swaption/swaptionvolmatrix.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::swaptionvolmatrix(py::module_& m) {
    // Linear child of py::classh parent (SwaptionVolatilityDiscrete),
    // uses standard py::class_ with shared_ptr holder.
    py::class_<SwaptionVolatilityMatrix, SwaptionVolatilityDiscrete,
               ext::shared_ptr<SwaptionVolatilityMatrix>>(
        m, "SwaptionVolatilityMatrix",
        "Discrete swaption volatility surface backed by a matrix.")
        // Floating reference date + Matrix data
        .def(py::init<const Calendar&, BusinessDayConvention,
                      const std::vector<Period>&, const std::vector<Period>&,
                      const Matrix&, const DayCounter&,
                      bool, VolatilityType, const Matrix&>(),
            py::arg("calendar"), py::arg("businessDayConvention"),
            py::arg("optionTenors"), py::arg("swapTenors"),
            py::arg("volatilities"), py::arg("dayCounter"),
            py::arg("flatExtrapolation") = false,
            py::arg("type") = ShiftedLognormal,
            py::arg("shifts") = Matrix(),
            "Constructs from calendar with fixed volatility matrix.")
        // Fixed reference date + Matrix data
        .def(py::init<const Date&, const Calendar&, BusinessDayConvention,
                      const std::vector<Period>&, const std::vector<Period>&,
                      const Matrix&, const DayCounter&,
                      bool, VolatilityType, const Matrix&>(),
            py::arg("referenceDate"), py::arg("calendar"),
            py::arg("businessDayConvention"),
            py::arg("optionTenors"), py::arg("swapTenors"),
            py::arg("volatilities"), py::arg("dayCounter"),
            py::arg("flatExtrapolation") = false,
            py::arg("type") = ShiftedLognormal,
            py::arg("shifts") = Matrix(),
            "Constructs from reference date with fixed volatility matrix.")
        // Floating reference date + Quote handles
        .def(py::init<const Calendar&, BusinessDayConvention,
                      const std::vector<Period>&, const std::vector<Period>&,
                      const std::vector<std::vector<Handle<Quote>>>&,
                      const DayCounter&,
                      bool, VolatilityType,
                      const std::vector<std::vector<Real>>&>(),
            py::arg("calendar"), py::arg("businessDayConvention"),
            py::arg("optionTenors"), py::arg("swapTenors"),
            py::arg("volatilities"), py::arg("dayCounter"),
            py::arg("flatExtrapolation") = false,
            py::arg("type") = ShiftedLognormal,
            py::arg("shifts") = std::vector<std::vector<Real>>(),
            "Constructs from calendar with quote handle matrix.")
        // Fixed reference date + Quote handles
        .def(py::init<const Date&, const Calendar&, BusinessDayConvention,
                      const std::vector<Period>&, const std::vector<Period>&,
                      const std::vector<std::vector<Handle<Quote>>>&,
                      const DayCounter&,
                      bool, VolatilityType,
                      const std::vector<std::vector<Real>>&>(),
            py::arg("referenceDate"), py::arg("calendar"),
            py::arg("businessDayConvention"),
            py::arg("optionTenors"), py::arg("swapTenors"),
            py::arg("volatilities"), py::arg("dayCounter"),
            py::arg("flatExtrapolation") = false,
            py::arg("type") = ShiftedLognormal,
            py::arg("shifts") = std::vector<std::vector<Real>>(),
            "Constructs from reference date with quote handle matrix.")
        // Fixed reference date + option dates + Matrix data
        .def(py::init<const Date&, const Calendar&, BusinessDayConvention,
                      const std::vector<Date>&, const std::vector<Period>&,
                      const Matrix&, const DayCounter&,
                      bool, VolatilityType, const Matrix&>(),
            py::arg("referenceDate"), py::arg("calendar"),
            py::arg("businessDayConvention"),
            py::arg("optionDates"), py::arg("swapTenors"),
            py::arg("volatilities"), py::arg("dayCounter"),
            py::arg("flatExtrapolation") = false,
            py::arg("type") = ShiftedLognormal,
            py::arg("shifts") = Matrix(),
            "Constructs from reference date with option dates and matrix.")
        .def("locate",
            py::overload_cast<const Date&, const Period&>(
                &SwaptionVolatilityMatrix::locate, py::const_),
            py::arg("optionDate"), py::arg("swapTenor"),
            "Returns row/column index pair for given option date and swap tenor.")
        .def("locate",
            py::overload_cast<Time, Time>(
                &SwaptionVolatilityMatrix::locate, py::const_),
            py::arg("optionTime"), py::arg("swapLength"),
            "Returns row/column index pair for given option time and swap length.");
}
