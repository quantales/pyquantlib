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
#include <ql/pricingengines/vanilla/fdsabrvanillaengine.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::fdsabrvanillaengine(py::module_& m) {
    py::class_<FdSabrVanillaEngine,
               ext::shared_ptr<FdSabrVanillaEngine>,
               PricingEngine>(
        m, "FdSabrVanillaEngine",
        "Finite-differences SABR vanilla option engine.")
        // Handle constructor
        .def(py::init<Real, Real, Real, Real, Real,
                      Handle<YieldTermStructure>,
                      Size, Size, Size, Size, Real, Real,
                      const FdmSchemeDesc&>(),
            py::arg("f0"),
            py::arg("alpha"),
            py::arg("beta"),
            py::arg("nu"),
            py::arg("rho"),
            py::arg("rTS"),
            py::arg("tGrid") = 50,
            py::arg("fGrid") = 400,
            py::arg("xGrid") = 50,
            py::arg("dampingSteps") = 0,
            py::arg("scalingFactor") = 1.0,
            py::arg("eps") = 1e-4,
            py::arg("schemeDesc") = FdmSchemeDesc::Hundsdorfer(),
            "Constructs FD SABR engine with handle.")
        // Hidden handle constructor
        .def(py::init([](Real f0, Real alpha, Real beta, Real nu, Real rho,
                        const ext::shared_ptr<YieldTermStructure>& rTS,
                        Size tGrid, Size fGrid, Size xGrid,
                        Size dampingSteps, Real scalingFactor, Real eps,
                        const FdmSchemeDesc& schemeDesc) {
            return ext::make_shared<FdSabrVanillaEngine>(
                f0, alpha, beta, nu, rho,
                Handle<YieldTermStructure>(rTS),
                tGrid, fGrid, xGrid, dampingSteps,
                scalingFactor, eps, schemeDesc);
        }),
            py::arg("f0"),
            py::arg("alpha"),
            py::arg("beta"),
            py::arg("nu"),
            py::arg("rho"),
            py::arg("rTS"),
            py::arg("tGrid") = 50,
            py::arg("fGrid") = 400,
            py::arg("xGrid") = 50,
            py::arg("dampingSteps") = 0,
            py::arg("scalingFactor") = 1.0,
            py::arg("eps") = 1e-4,
            py::arg("schemeDesc") = FdmSchemeDesc::Hundsdorfer(),
            "Constructs FD SABR engine (handle created internally).");
}
