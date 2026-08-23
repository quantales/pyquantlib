/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/pricingengines/asian/fdblackscholesasianengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/methods/finitedifferences/solvers/fdmbackwardsolver.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::fdblackscholesasianengine(py::module_& m) {
    py::class_<FdBlackScholesAsianEngine,
               PricingEngine,
               ext::shared_ptr<FdBlackScholesAsianEngine>>(
        m, "FdBlackScholesAsianEngine",
        "Finite-difference Black-Scholes discrete Asian engine.")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      Size, Size, Size, const FdmSchemeDesc&>(),
            py::arg("process"),
            py::arg("tGrid") = 100,
            py::arg("xGrid") = 100,
            py::arg("aGrid") = 50,
            py::arg("schemeDesc") = FdmSchemeDesc::Douglas(),
            "Constructs engine.");
}
