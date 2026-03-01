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
#include <ql/methods/finitedifferences/operators/fdmlinearop.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmlinearop(py::module_& m) {
    py::class_<FdmLinearOp, ext::shared_ptr<FdmLinearOp>>(
        m, "FdmLinearOp",
        "Abstract base class for FDM linear operators.")
        .def("apply", &FdmLinearOp::apply,
            py::arg("r"),
            "Applies the operator to an array.");
}
