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
#include <ql/methods/finitedifferences/operators/fdmsquarerootfwdop.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmsquarerootfwdop(py::module_& m) {
    py::enum_<FdmSquareRootFwdOp::TransformationType>(
        m, "FdmSquareRootFwdOpTransformationType",
        "Coordinate transformation for square-root process FD scheme.")
        .value("Plain", FdmSquareRootFwdOp::Plain)
        .value("Power", FdmSquareRootFwdOp::Power)
        .value("Log", FdmSquareRootFwdOp::Log);
}
