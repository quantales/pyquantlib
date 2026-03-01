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
#include <ql/methods/finitedifferences/operators/fdmhestonhullwhiteop.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <ql/processes/hestonprocess.hpp>
#include <ql/processes/hullwhiteprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmhestonhullwhiteop(py::module_& m) {
    py::class_<FdmHestonHullWhiteOp, FdmLinearOpComposite,
               ext::shared_ptr<FdmHestonHullWhiteOp>>(
        m, "FdmHestonHullWhiteOp",
        "Heston-Hull-White FDM operator.")
        .def(py::init<const ext::shared_ptr<FdmMesher>&,
                       const ext::shared_ptr<HestonProcess>&,
                       const ext::shared_ptr<HullWhiteProcess>&,
                       Real>(),
            py::arg("mesher"), py::arg("hestonProcess"),
            py::arg("hwProcess"), py::arg("equityShortRateCorrelation"),
            "Constructs a Heston-Hull-White operator.");
}
