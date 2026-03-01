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
#include <ql/methods/finitedifferences/solvers/fdm3dimsolver.hpp>
#include <ql/methods/finitedifferences/operators/fdmlinearopcomposite.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdm3dimsolver(py::module_& m) {
    py::class_<Fdm3DimSolver,
               ext::shared_ptr<Fdm3DimSolver>,
               LazyObject>(
        m, "Fdm3DimSolver",
        "3D FDM solver with bicubic spline interpolation.")
        .def(py::init<const FdmSolverDesc&,
                      const FdmSchemeDesc&,
                      ext::shared_ptr<FdmLinearOpComposite>>(),
            py::arg("solverDesc"),
            py::arg("schemeDesc"),
            py::arg("op"),
            "Constructs with solver descriptor, scheme descriptor, and operator.")
        .def("interpolateAt", &Fdm3DimSolver::interpolateAt,
            py::arg("x"), py::arg("y"), py::arg("z"),
            "Interpolates solution at coordinates (x, y, z).")
        .def("thetaAt", &Fdm3DimSolver::thetaAt,
            py::arg("x"), py::arg("y"), py::arg("z"),
            "Returns theta at coordinates (x, y, z).");
}
