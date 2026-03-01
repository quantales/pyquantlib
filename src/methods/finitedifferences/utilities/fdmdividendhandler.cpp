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
#include <ql/methods/finitedifferences/utilities/fdmdividendhandler.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <ql/time/daycounter.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmdividendhandler(py::module_& m) {
    py::class_<FdmDividendHandler,
               ext::shared_ptr<FdmDividendHandler>,
               StepCondition<Array>>(
        m, "FdmDividendHandler",
        "Applies discrete dividends as a step condition.")
        .def(py::init<const DividendSchedule&,
                      const ext::shared_ptr<FdmMesher>&,
                      const Date&,
                      const DayCounter&,
                      Size>(),
            py::arg("schedule"),
            py::arg("mesher"),
            py::arg("referenceDate"),
            py::arg("dayCounter"),
            py::arg("equityDirection"),
            "Constructs with dividend schedule, mesher, reference date, day counter, and equity direction.")
        .def("dividendTimes", &FdmDividendHandler::dividendTimes,
            py::return_value_policy::reference_internal,
            "Returns dividend payment times.")
        .def("dividendDates", &FdmDividendHandler::dividendDates,
            py::return_value_policy::reference_internal,
            "Returns dividend payment dates.")
        .def("dividends", &FdmDividendHandler::dividends,
            py::return_value_policy::reference_internal,
            "Returns dividend amounts.");
}
