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
#include <ql/methods/finitedifferences/operators/fdmg2op.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <ql/models/shortrate/twofactormodels/g2.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmg2op(py::module_& m) {
    py::class_<FdmG2Op, FdmLinearOpComposite,
               ext::shared_ptr<FdmG2Op>>(
        m, "FdmG2Op",
        "G2++ two-factor interest rate FDM operator.")
        .def(py::init<const ext::shared_ptr<FdmMesher>&,
                       const ext::shared_ptr<G2>&,
                       Size, Size>(),
            py::arg("mesher"), py::arg("model"),
            py::arg("direction1"), py::arg("direction2"),
            "Constructs a G2 operator.");
}
