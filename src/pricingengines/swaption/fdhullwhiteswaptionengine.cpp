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
#include <ql/pricingengines/swaption/fdhullwhiteswaptionengine.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::fdhullwhiteswaptionengine(py::module_& m) {
    py::class_<FdHullWhiteSwaptionEngine, PricingEngine,
               ext::shared_ptr<FdHullWhiteSwaptionEngine>>(
        m, "FdHullWhiteSwaptionEngine",
        "Finite-differences swaption engine for Hull-White model.")
        .def(py::init<const ext::shared_ptr<HullWhite>&, Size, Size, Size, Real,
                      const FdmSchemeDesc&>(),
            py::arg("model"),
            py::arg("tGrid") = 100,
            py::arg("xGrid") = 100,
            py::arg("dampingSteps") = 0,
            py::arg("invEps") = 1e-5,
            py::arg("schemeDesc") = FdmSchemeDesc::Douglas(),
            "Constructs FD Hull-White swaption engine.");
}
