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
#include <ql/methods/finitedifferences/stepconditions/fdmsimpleswingcondition.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <ql/methods/finitedifferences/utilities/fdminnervaluecalculator.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmsimpleswingcondition(py::module_& m) {
    py::class_<FdmSimpleSwingCondition,
               ext::shared_ptr<FdmSimpleSwingCondition>,
               StepCondition<Array>>(
        m, "FdmSimpleSwingCondition",
        "Simple swing option step condition for FDM pricing.")
        .def(py::init<std::vector<Time>,
                       ext::shared_ptr<FdmMesher>,
                       ext::shared_ptr<FdmInnerValueCalculator>,
                       Size, Size>(),
            py::arg("exerciseTimes"), py::arg("mesher"),
            py::arg("calculator"), py::arg("swingDirection"),
            py::arg("minExercises") = 0,
            "Constructs with exercise times, mesher, calculator, "
            "swing direction index, and minimum exercises.");
}
