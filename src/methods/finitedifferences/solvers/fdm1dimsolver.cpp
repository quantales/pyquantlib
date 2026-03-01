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
#include <ql/methods/finitedifferences/solvers/fdm1dimsolver.hpp>
#include <ql/methods/finitedifferences/operators/fdmlinearopcomposite.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdm1dimsolver(py::module_& m) {
    py::class_<Fdm1DimSolver,
               ext::shared_ptr<Fdm1DimSolver>,
               LazyObject>(
        m, "Fdm1DimSolver",
        "1D FDM solver with cubic interpolation.")
        .def(py::init<const FdmSolverDesc&,
                      const FdmSchemeDesc&,
                      ext::shared_ptr<FdmLinearOpComposite>>(),
            py::arg("solverDesc"),
            py::arg("schemeDesc"),
            py::arg("op"),
            "Constructs with solver descriptor, scheme descriptor, and operator.")
        .def("interpolateAt", &Fdm1DimSolver::interpolateAt,
            py::arg("x"),
            "Interpolates solution at coordinate x.")
        .def("thetaAt", &Fdm1DimSolver::thetaAt,
            py::arg("x"),
            "Returns theta at coordinate x.")
        .def("derivativeX", &Fdm1DimSolver::derivativeX,
            py::arg("x"),
            "Returns first derivative at coordinate x.")
        .def("derivativeXX", &Fdm1DimSolver::derivativeXX,
            py::arg("x"),
            "Returns second derivative at coordinate x.");
}
