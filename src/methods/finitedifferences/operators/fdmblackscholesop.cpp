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
#include <ql/methods/finitedifferences/operators/fdmblackscholesop.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <ql/methods/finitedifferences/utilities/fdmquantohelper.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmblackscholesop(py::module_& m) {
    py::class_<FdmBlackScholesOp, FdmLinearOpComposite,
               ext::shared_ptr<FdmBlackScholesOp>>(
        m, "FdmBlackScholesOp",
        "Black-Scholes FDM operator.")
        .def(py::init([](const ext::shared_ptr<FdmMesher>& mesher,
                         const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
                         Real strike,
                         bool localVol,
                         const py::object& illegalLocalVolOverwrite,
                         Size direction,
                         ext::shared_ptr<FdmQuantoHelper> quantoHelper) {
            Real overwrite = -Null<Real>();
            if (!illegalLocalVolOverwrite.is_none())
                overwrite = illegalLocalVolOverwrite.cast<Real>();
            return ext::make_shared<FdmBlackScholesOp>(
                mesher, process, strike, localVol, overwrite,
                direction, std::move(quantoHelper));
        }),
            py::arg("mesher"), py::arg("process"), py::arg("strike"),
            py::arg("localVol") = false,
            py::arg("illegalLocalVolOverwrite") = py::none(),
            py::arg("direction") = 0,
            py::arg("quantoHelper") = ext::shared_ptr<FdmQuantoHelper>(),
            "Constructs a Black-Scholes operator.");
}
