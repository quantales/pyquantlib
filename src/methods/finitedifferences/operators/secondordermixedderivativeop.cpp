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
#include <ql/methods/finitedifferences/operators/secondordermixedderivativeop.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::secondordermixedderivativeop(py::module_& m) {
    py::class_<SecondOrderMixedDerivativeOp, NinePointLinearOp,
               ext::shared_ptr<SecondOrderMixedDerivativeOp>>(
        m, "SecondOrderMixedDerivativeOp",
        "Second-order mixed derivative operator for 2D FDM grids.")
        .def(py::init<Size, Size, const ext::shared_ptr<FdmMesher>&>(),
            py::arg("d0"), py::arg("d1"), py::arg("mesher"),
            "Constructs from two directions and a mesher.");
}
