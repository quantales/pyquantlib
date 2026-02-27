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
#include <ql/pricingengines/vanilla/fdcevvanillaengine.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::fdcevvanillaengine(py::module_& m) {
    py::class_<FdCEVVanillaEngine,
               ext::shared_ptr<FdCEVVanillaEngine>,
               PricingEngine>(
        m, "FdCEVVanillaEngine",
        "Finite-differences CEV vanilla option engine.")
        // Handle constructor
        .def(py::init<Real, Real, Real,
                      Handle<YieldTermStructure>,
                      Size, Size, Size, Real, Real,
                      const FdmSchemeDesc&>(),
            py::arg("f0"),
            py::arg("alpha"),
            py::arg("beta"),
            py::arg("discountCurve"),
            py::arg("tGrid") = 50,
            py::arg("xGrid") = 400,
            py::arg("dampingSteps") = 0,
            py::arg("scalingFactor") = 1.0,
            py::arg("eps") = 1e-4,
            py::arg("schemeDesc") = FdmSchemeDesc::Douglas(),
            "Constructs FD CEV engine with handle.")
        // Hidden handle constructor
        .def(py::init([](Real f0, Real alpha, Real beta,
                        const ext::shared_ptr<YieldTermStructure>& discountCurve,
                        Size tGrid, Size xGrid,
                        Size dampingSteps, Real scalingFactor, Real eps,
                        const FdmSchemeDesc& schemeDesc) {
            return ext::make_shared<FdCEVVanillaEngine>(
                f0, alpha, beta,
                Handle<YieldTermStructure>(discountCurve),
                tGrid, xGrid, dampingSteps,
                scalingFactor, eps, schemeDesc);
        }),
            py::arg("f0"),
            py::arg("alpha"),
            py::arg("beta"),
            py::arg("discountCurve"),
            py::arg("tGrid") = 50,
            py::arg("xGrid") = 400,
            py::arg("dampingSteps") = 0,
            py::arg("scalingFactor") = 1.0,
            py::arg("eps") = 1e-4,
            py::arg("schemeDesc") = FdmSchemeDesc::Douglas(),
            "Constructs FD CEV engine (handle created internally).");
}
