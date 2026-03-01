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
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
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

    py::class_<FdmSquareRootFwdOp, FdmLinearOpComposite,
               ext::shared_ptr<FdmSquareRootFwdOp>>(
        m, "FdmSquareRootFwdOp",
        "Square-root process Fokker-Planck forward operator.")
        .def(py::init<const ext::shared_ptr<FdmMesher>&,
                       Real, Real, Real, Size,
                       FdmSquareRootFwdOp::TransformationType>(),
            py::arg("mesher"), py::arg("kappa"), py::arg("theta"),
            py::arg("sigma"), py::arg("direction"),
            py::arg("type") = FdmSquareRootFwdOp::Plain,
            "Constructs a square-root forward operator.")
        .def("lowerBoundaryFactor", &FdmSquareRootFwdOp::lowerBoundaryFactor,
            py::arg("type") = FdmSquareRootFwdOp::Plain,
            "Returns the lower boundary factor.")
        .def("upperBoundaryFactor", &FdmSquareRootFwdOp::upperBoundaryFactor,
            py::arg("type") = FdmSquareRootFwdOp::Plain,
            "Returns the upper boundary factor.")
        .def("v", &FdmSquareRootFwdOp::v,
            py::arg("i"),
            "Returns the transformed value at index i.");
}
