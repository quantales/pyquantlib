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
#include <ql/pricingengines/basket/fdndimblackscholesvanillaengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/math/matrix.hpp>
#include <ql/methods/finitedifferences/solvers/fdmbackwardsolver.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::fdndimblackscholesvanillaengine(py::module_& m) {
    py::class_<FdndimBlackScholesVanillaEngine, PricingEngine,
               ext::shared_ptr<FdndimBlackScholesVanillaEngine>>(
        m, "FdndimBlackScholesVanillaEngine",
        "N-dimensional finite-difference Black-Scholes basket engine.")
        .def(py::init<std::vector<ext::shared_ptr<GeneralizedBlackScholesProcess>>,
                      Matrix, std::vector<Size>, Size, Size, const FdmSchemeDesc&>(),
            py::arg("processes"),
            py::arg("rho"),
            py::arg("xGrids"),
            py::arg("tGrid") = 50,
            py::arg("dampingSteps") = 0,
            py::arg("schemeDesc") = FdmSchemeDesc::Douglas(),
            "Constructs with explicit per-dimension grid sizes.")
        .def(py::init<std::vector<ext::shared_ptr<GeneralizedBlackScholesProcess>>,
                      Matrix, Size, Size, Size, const FdmSchemeDesc&>(),
            py::arg("processes"),
            py::arg("rho"),
            py::arg("xGrid"),
            py::arg("tGrid") = 50,
            py::arg("dampingSteps") = 0,
            py::arg("schemeDesc") = FdmSchemeDesc::Douglas(),
            "Constructs with auto-scaling grid sizes.");
}
