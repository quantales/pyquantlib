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
#include <ql/methods/finitedifferences/stepconditions/fdmbermudanstepcondition.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <ql/methods/finitedifferences/utilities/fdminnervaluecalculator.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmbermudanstepcondition(py::module_& m) {
    py::class_<FdmBermudanStepCondition,
               ext::shared_ptr<FdmBermudanStepCondition>,
               StepCondition<Array>>(
        m, "FdmBermudanStepCondition",
        "Bermudan-style early exercise step condition.")
        .def(py::init<const std::vector<Date>&,
                      const Date&,
                      const DayCounter&,
                      ext::shared_ptr<FdmMesher>,
                      ext::shared_ptr<FdmInnerValueCalculator>>(),
            py::arg("exerciseDates"),
            py::arg("referenceDate"),
            py::arg("dayCounter"),
            py::arg("mesher"),
            py::arg("calculator"),
            "Constructs with exercise dates, reference date, day counter, mesher, and calculator.")
        .def("exerciseTimes", &FdmBermudanStepCondition::exerciseTimes,
            py::return_value_policy::reference_internal,
            "Returns exercise times.");
}
