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
#include <ql/methods/finitedifferences/operators/fdmhestonfwdop.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <ql/processes/hestonprocess.hpp>
#include <ql/termstructures/volatility/equityfx/localvoltermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmhestonfwdop(py::module_& m) {
    py::class_<FdmHestonFwdOp, FdmLinearOpComposite,
               ext::shared_ptr<FdmHestonFwdOp>>(
        m, "FdmHestonFwdOp",
        "Heston Fokker-Planck forward operator.")
        .def(py::init<const ext::shared_ptr<FdmMesher>&,
                       const ext::shared_ptr<HestonProcess>&,
                       FdmSquareRootFwdOp::TransformationType,
                       ext::shared_ptr<LocalVolTermStructure>,
                       Real>(),
            py::arg("mesher"), py::arg("process"),
            py::arg("type") = FdmSquareRootFwdOp::Plain,
            py::arg("leverageFct") = ext::shared_ptr<LocalVolTermStructure>(),
            py::arg("mixingFactor") = 1.0,
            "Constructs a Heston forward operator.");
}
