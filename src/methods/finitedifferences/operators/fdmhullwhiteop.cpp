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
#include <ql/methods/finitedifferences/operators/fdmhullwhiteop.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <ql/models/shortrate/onefactormodels/hullwhite.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmhullwhiteop(py::module_& m) {
    py::class_<FdmHullWhiteOp, FdmLinearOpComposite,
               ext::shared_ptr<FdmHullWhiteOp>>(
        m, "FdmHullWhiteOp",
        "Hull-White interest rate FDM operator.")
        .def(py::init<const ext::shared_ptr<FdmMesher>&,
                       const ext::shared_ptr<HullWhite>&,
                       Size>(),
            py::arg("mesher"), py::arg("model"), py::arg("direction"),
            "Constructs a Hull-White operator.");
}
