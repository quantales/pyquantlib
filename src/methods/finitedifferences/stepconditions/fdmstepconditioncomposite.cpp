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
#include <ql/methods/finitedifferences/stepconditions/fdmstepconditioncomposite.hpp>
#include <ql/methods/finitedifferences/stepconditions/fdmsnapshotcondition.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <ql/methods/finitedifferences/utilities/fdminnervaluecalculator.hpp>
#include <ql/exercise.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmstepconditioncomposite(py::module_& m) {
    using Conditions = FdmStepConditionComposite::Conditions;

    py::class_<FdmStepConditionComposite,
               ext::shared_ptr<FdmStepConditionComposite>,
               StepCondition<Array>>(
        m, "FdmStepConditionComposite",
        "Composite of FDM step conditions.")
        .def(py::init<const std::list<std::vector<Time>>&,
                      Conditions>(),
            py::arg("stoppingTimes"), py::arg("conditions"),
            "Constructs from stopping times and conditions.")
        .def("stoppingTimes", &FdmStepConditionComposite::stoppingTimes,
            py::return_value_policy::reference_internal,
            "Returns merged stopping times.")
        .def("conditions", &FdmStepConditionComposite::conditions,
            py::return_value_policy::reference_internal,
            "Returns the list of conditions.")
        .def_static("joinConditions",
            &FdmStepConditionComposite::joinConditions,
            py::arg("snapshotCondition"), py::arg("composite"),
            "Joins a snapshot condition with an existing composite.")
        .def_static("vanillaComposite",
            &FdmStepConditionComposite::vanillaComposite,
            py::arg("dividendSchedule"),
            py::arg("exercise"),
            py::arg("mesher"),
            py::arg("calculator"),
            py::arg("referenceDate"),
            py::arg("dayCounter"),
            "Creates a standard composite for vanilla option FDM pricing.");
}
