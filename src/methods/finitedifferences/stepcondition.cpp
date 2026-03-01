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
#include <ql/methods/finitedifferences/stepcondition.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::stepcondition(py::module_& m) {
    py::class_<StepCondition<Array>,
               ext::shared_ptr<StepCondition<Array>>>(
        m, "FdmStepCondition",
        "Step condition applied at each time step during FDM rollback.")
        .def("applyTo", [](const StepCondition<Array>& self,
                           Array a, Time t) {
            self.applyTo(a, t);
            return a;
        }, py::arg("a"), py::arg("t"),
            "Applies condition to array at time t (returns modified copy).");
}
