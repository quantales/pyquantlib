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
#include <ql/methods/finitedifferences/utilities/fdmdiscountdirichletboundary.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

using FdmBoundaryCondition = BoundaryCondition<FdmLinearOp>;

void ql_methods::fdmdiscountdirichletboundary(py::module_& m) {
    py::class_<FdmDiscountDirichletBoundary,
               ext::shared_ptr<FdmDiscountDirichletBoundary>,
               FdmBoundaryCondition>(
        m, "FdmDiscountDirichletBoundary",
        "Discounted Dirichlet boundary condition for FDM.")
        .def(py::init<ext::shared_ptr<FdmMesher>,
                       ext::shared_ptr<YieldTermStructure>,
                       Time, Real, Size, FdmBoundaryCondition::Side>(),
            py::arg("mesher"), py::arg("rTS"),
            py::arg("maturityTime"), py::arg("valueOnBoundary"),
            py::arg("direction"), py::arg("side"),
            "Constructs with mesher, yield curve, maturity time, "
            "boundary value, direction, and side.");
}
