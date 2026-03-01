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
#include <ql/methods/finitedifferences/operators/fdmsabrop.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmsabrop(py::module_& m) {
    py::class_<FdmSabrOp, FdmLinearOpComposite,
               ext::shared_ptr<FdmSabrOp>>(
        m, "FdmSabrOp",
        "SABR stochastic volatility FDM operator.")
        .def(py::init<const ext::shared_ptr<FdmMesher>&,
                       ext::shared_ptr<YieldTermStructure>,
                       Real, Real, Real, Real, Real>(),
            py::arg("mesher"), py::arg("rTS"),
            py::arg("f0"), py::arg("alpha"), py::arg("beta"),
            py::arg("nu"), py::arg("rho"),
            "Constructs a SABR operator.");
}
