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
#include <ql/methods/finitedifferences/solvers/fdm2dimsolver.hpp>
#include <ql/methods/finitedifferences/operators/fdmlinearopcomposite.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdm2dimsolver(py::module_& m) {
    py::class_<Fdm2DimSolver,
               ext::shared_ptr<Fdm2DimSolver>,
               LazyObject>(
        m, "Fdm2DimSolver",
        "2D FDM solver with bicubic spline interpolation.")
        .def(py::init<const FdmSolverDesc&,
                      const FdmSchemeDesc&,
                      ext::shared_ptr<FdmLinearOpComposite>>(),
            py::arg("solverDesc"),
            py::arg("schemeDesc"),
            py::arg("op"),
            "Constructs with solver descriptor, scheme descriptor, and operator.")
        .def("interpolateAt", &Fdm2DimSolver::interpolateAt,
            py::arg("x"), py::arg("y"),
            "Interpolates solution at coordinates (x, y).")
        .def("thetaAt", &Fdm2DimSolver::thetaAt,
            py::arg("x"), py::arg("y"),
            "Returns theta at coordinates (x, y).")
        .def("derivativeX", &Fdm2DimSolver::derivativeX,
            py::arg("x"), py::arg("y"),
            "Returns first derivative w.r.t. x.")
        .def("derivativeY", &Fdm2DimSolver::derivativeY,
            py::arg("x"), py::arg("y"),
            "Returns first derivative w.r.t. y.")
        .def("derivativeXX", &Fdm2DimSolver::derivativeXX,
            py::arg("x"), py::arg("y"),
            "Returns second derivative w.r.t. x.")
        .def("derivativeYY", &Fdm2DimSolver::derivativeYY,
            py::arg("x"), py::arg("y"),
            "Returns second derivative w.r.t. y.")
        .def("derivativeXY", &Fdm2DimSolver::derivativeXY,
            py::arg("x"), py::arg("y"),
            "Returns cross derivative w.r.t. x and y.");
}
