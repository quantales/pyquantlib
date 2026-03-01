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
#include <ql/methods/finitedifferences/stepconditions/fdmsnapshotcondition.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmsnapshotcondition(py::module_& m) {
    py::class_<FdmSnapshotCondition,
               ext::shared_ptr<FdmSnapshotCondition>,
               StepCondition<Array>>(
        m, "FdmSnapshotCondition",
        "Captures array values at a specific time (for theta calculation).")
        .def(py::init<Time>(),
            py::arg("t"),
            "Constructs with snapshot time.")
        .def("getTime", &FdmSnapshotCondition::getTime,
            "Returns the snapshot time.")
        .def("getValues", &FdmSnapshotCondition::getValues,
            py::return_value_policy::reference_internal,
            "Returns the captured values.");
}
