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
#include <ql/methods/finitedifferences/operators/fdmblackscholesfwdop.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmblackscholesfwdop(py::module_& m) {
    py::class_<FdmBlackScholesFwdOp, FdmLinearOpComposite,
               ext::shared_ptr<FdmBlackScholesFwdOp>>(
        m, "FdmBlackScholesFwdOp",
        "Black-Scholes Fokker-Planck forward operator.")
        .def(py::init([](const ext::shared_ptr<FdmMesher>& mesher,
                         const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
                         Real strike,
                         bool localVol,
                         const py::object& illegalLocalVolOverwrite,
                         Size direction) {
            Real overwrite = -Null<Real>();
            if (!illegalLocalVolOverwrite.is_none())
                overwrite = illegalLocalVolOverwrite.cast<Real>();
            return ext::make_shared<FdmBlackScholesFwdOp>(
                mesher, process, strike, localVol, overwrite, direction);
        }),
            py::arg("mesher"), py::arg("process"), py::arg("strike"),
            py::arg("localVol") = false,
            py::arg("illegalLocalVolOverwrite") = py::none(),
            py::arg("direction") = 0,
            "Constructs a Black-Scholes forward operator.");
}
