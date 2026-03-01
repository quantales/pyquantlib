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
#include <ql/methods/finitedifferences/stepconditions/fdmamericanstepcondition.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <ql/methods/finitedifferences/utilities/fdminnervaluecalculator.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmamericanstepcondition(py::module_& m) {
    py::class_<FdmAmericanStepCondition,
               ext::shared_ptr<FdmAmericanStepCondition>,
               StepCondition<Array>>(
        m, "FdmAmericanStepCondition",
        "American-style early exercise step condition.")
        .def(py::init<ext::shared_ptr<FdmMesher>,
                      ext::shared_ptr<FdmInnerValueCalculator>>(),
            py::arg("mesher"), py::arg("calculator"),
            "Constructs with mesher and inner value calculator.");
}
