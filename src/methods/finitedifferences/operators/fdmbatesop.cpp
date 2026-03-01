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
#include <ql/methods/finitedifferences/operators/fdmbatesop.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <ql/methods/finitedifferences/utilities/fdmquantohelper.hpp>
#include <ql/methods/finitedifferences/utilities/fdmboundaryconditionset.hpp>
#include <ql/processes/batesprocess.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmbatesop(py::module_& m) {
    py::class_<FdmBatesOp, FdmLinearOpComposite,
               ext::shared_ptr<FdmBatesOp>>(
        m, "FdmBatesOp",
        "Bates (Heston + jumps) FDM operator.")
        .def(py::init<const ext::shared_ptr<FdmMesher>&,
                       const ext::shared_ptr<BatesProcess>&,
                       FdmBoundaryConditionSet,
                       Size,
                       const ext::shared_ptr<FdmQuantoHelper>&>(),
            py::arg("mesher"), py::arg("batesProcess"),
            py::arg("bcSet"), py::arg("integroIntegrationOrder"),
            py::arg("quantoHelper") = ext::shared_ptr<FdmQuantoHelper>(),
            "Constructs a Bates operator.");
}
