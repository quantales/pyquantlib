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
#include <ql/pricingengines/swaption/fdg2swaptionengine.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::fdg2swaptionengine(py::module_& m) {
    py::class_<FdG2SwaptionEngine, PricingEngine,
               ext::shared_ptr<FdG2SwaptionEngine>>(
        m, "FdG2SwaptionEngine",
        "Finite-differences swaption engine for G2++ two-factor model.")
        .def(py::init<const ext::shared_ptr<G2>&, Size, Size, Size, Size, Real,
                      const FdmSchemeDesc&>(),
            py::arg("model"),
            py::arg("tGrid") = 100,
            py::arg("xGrid") = 50,
            py::arg("yGrid") = 50,
            py::arg("dampingSteps") = 0,
            py::arg("invEps") = 1e-5,
            py::arg("schemeDesc") = FdmSchemeDesc::Hundsdorfer(),
            "Constructs FD G2 swaption engine.");
}
