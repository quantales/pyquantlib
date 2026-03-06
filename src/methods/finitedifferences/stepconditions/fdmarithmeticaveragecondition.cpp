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
#include <ql/methods/finitedifferences/stepconditions/fdmarithmeticaveragecondition.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmarithmeticaveragecondition(py::module_& m) {
    py::class_<FdmArithmeticAverageCondition,
               ext::shared_ptr<FdmArithmeticAverageCondition>,
               StepCondition<Array>>(
        m, "FdmArithmeticAverageCondition",
        "Arithmetic average step condition for Asian option FDM pricing.")
        .def(py::init<std::vector<Time>, Real, Size,
                       ext::shared_ptr<FdmMesher>, Size>(),
            py::arg("averageTimes"), py::arg("runningAverage"),
            py::arg("pastFixings"), py::arg("mesher"),
            py::arg("equityDirection"),
            "Constructs with averaging times, running average, "
            "past fixings, mesher, and equity direction index.");
}
