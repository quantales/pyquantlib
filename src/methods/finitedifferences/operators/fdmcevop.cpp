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
#include <ql/methods/finitedifferences/operators/fdmcevop.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmcevop(py::module_& m) {
    // FdmCEVOp stores rTS_ as a const reference to the shared_ptr passed
    // to the constructor.  When constructed via pybind11, the shared_ptr
    // is a temporary that dies after the constructor returns, leaving a
    // dangling reference.  Use an aliased shared_ptr to keep the rTS
    // alive for the lifetime of the FdmCEVOp.
    py::class_<FdmCEVOp, FdmLinearOpComposite,
               ext::shared_ptr<FdmCEVOp>>(
        m, "FdmCEVOp",
        "Constant Elasticity of Variance FDM operator.")
        .def(py::init([](const ext::shared_ptr<FdmMesher>& mesher,
                         const ext::shared_ptr<YieldTermStructure>& rTS,
                         Real f0, Real alpha, Real beta, Size direction) {
            // Prevent dangling: store rTS in a shared_ptr that outlives
            // the FdmCEVOp via aliased pointer trick.
            auto rTSCopy = ext::make_shared<ext::shared_ptr<YieldTermStructure>>(rTS);
            auto op = ext::shared_ptr<FdmCEVOp>(
                new FdmCEVOp(mesher, *rTSCopy, f0, alpha, beta, direction),
                [rTSCopy](FdmCEVOp* p) { delete p; });
            return op;
        }),
            py::arg("mesher"), py::arg("rTS"),
            py::arg("f0"), py::arg("alpha"), py::arg("beta"),
            py::arg("direction"),
            "Constructs a CEV operator.");
}
