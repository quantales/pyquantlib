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
#include <ql/pricingengines/vanilla/fdsimplebsswingengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::fdsimplebsswingengine(py::module_& m) {
    py::class_<FdSimpleBSSwingEngine,
               ext::shared_ptr<FdSimpleBSSwingEngine>,
               PricingEngine>(
        m, "FdSimpleBSSwingEngine",
        "Finite-differences Black-Scholes engine for simple swing options.")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      Size, Size,
                      const FdmSchemeDesc&>(),
            py::arg("process"),
            py::arg("tGrid") = 50,
            py::arg("xGrid") = 100,
            py::arg("schemeDesc") = FdmSchemeDesc::Douglas(),
            "Constructs FD Black-Scholes swing option engine.");
}
