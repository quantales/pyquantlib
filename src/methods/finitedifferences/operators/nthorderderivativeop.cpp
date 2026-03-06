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
#include <ql/methods/finitedifferences/operators/nthorderderivativeop.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::nthorderderivativeop(py::module_& m) {
    py::class_<NthOrderDerivativeOp,
               ext::shared_ptr<NthOrderDerivativeOp>,
               FdmLinearOp>(
        m, "NthOrderDerivativeOp",
        "Nth-order finite difference derivative operator.")
        .def(py::init<Size, Size, Integer, ext::shared_ptr<FdmMesher>>(),
            py::arg("direction"), py::arg("order"),
            py::arg("nPoints"), py::arg("mesher"),
            "Constructs with direction, derivative order, stencil width, and mesher.");
}
