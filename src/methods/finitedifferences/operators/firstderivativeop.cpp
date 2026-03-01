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
#include <ql/methods/finitedifferences/operators/firstderivativeop.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::firstderivativeop(py::module_& m) {
    py::class_<FirstDerivativeOp, TripleBandLinearOp,
               ext::shared_ptr<FirstDerivativeOp>>(
        m, "FirstDerivativeOp",
        "First derivative operator on an FDM grid.")
        .def(py::init<Size, const ext::shared_ptr<FdmMesher>&>(),
            py::arg("direction"), py::arg("mesher"),
            "Constructs from direction and mesher.");
}
