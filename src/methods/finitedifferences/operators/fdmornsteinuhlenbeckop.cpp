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
#include <ql/methods/finitedifferences/operators/fdmornsteinuhlenbeckop.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <ql/processes/ornsteinuhlenbeckprocess.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmornsteinuhlenbeckop(py::module_& m) {
    py::class_<FdmOrnsteinUhlenbeckOp, FdmLinearOpComposite,
               ext::shared_ptr<FdmOrnsteinUhlenbeckOp>>(
        m, "FdmOrnsteinUhlenbeckOp",
        "Ornstein-Uhlenbeck process FDM operator.")
        .def(py::init<const ext::shared_ptr<FdmMesher>&,
                       ext::shared_ptr<OrnsteinUhlenbeckProcess>,
                       ext::shared_ptr<YieldTermStructure>,
                       Size>(),
            py::arg("mesher"), py::arg("process"),
            py::arg("rTS"), py::arg("direction") = 0,
            "Constructs an Ornstein-Uhlenbeck operator.");
}
