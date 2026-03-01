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
#include <ql/methods/finitedifferences/operators/fdmlocalvolfwdop.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/termstructures/volatility/equityfx/localvoltermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmlocalvolfwdop(py::module_& m) {
    py::class_<FdmLocalVolFwdOp, FdmLinearOpComposite,
               ext::shared_ptr<FdmLocalVolFwdOp>>(
        m, "FdmLocalVolFwdOp",
        "Local volatility Fokker-Planck forward operator.")
        .def(py::init<const ext::shared_ptr<FdmMesher>&,
                       const ext::shared_ptr<Quote>&,
                       ext::shared_ptr<YieldTermStructure>,
                       ext::shared_ptr<YieldTermStructure>,
                       const ext::shared_ptr<LocalVolTermStructure>&,
                       Size>(),
            py::arg("mesher"), py::arg("spot"),
            py::arg("rTS"), py::arg("qTS"),
            py::arg("localVol"), py::arg("direction") = 0,
            "Constructs a local volatility forward operator.");
}
