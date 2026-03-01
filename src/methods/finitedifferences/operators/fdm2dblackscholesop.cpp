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
#include <ql/methods/finitedifferences/operators/fdm2dblackscholesop.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdm2dblackscholesop(py::module_& m) {
    py::class_<Fdm2dBlackScholesOp, FdmLinearOpComposite,
               ext::shared_ptr<Fdm2dBlackScholesOp>>(
        m, "Fdm2dBlackScholesOp",
        "Two-dimensional Black-Scholes FDM operator.")
        .def(py::init([](const ext::shared_ptr<FdmMesher>& mesher,
                         const ext::shared_ptr<GeneralizedBlackScholesProcess>& p1,
                         const ext::shared_ptr<GeneralizedBlackScholesProcess>& p2,
                         Real correlation,
                         Time maturity,
                         bool localVol,
                         const py::object& illegalLocalVolOverwrite) {
            Real overwrite = -Null<Real>();
            if (!illegalLocalVolOverwrite.is_none())
                overwrite = illegalLocalVolOverwrite.cast<Real>();
            return ext::make_shared<Fdm2dBlackScholesOp>(
                mesher, p1, p2, correlation, maturity,
                localVol, overwrite);
        }),
            py::arg("mesher"), py::arg("p1"), py::arg("p2"),
            py::arg("correlation"), py::arg("maturity"),
            py::arg("localVol") = false,
            py::arg("illegalLocalVolOverwrite") = py::none(),
            "Constructs a 2D Black-Scholes operator.");
}
