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
#include <ql/pricingengines/swaption/g2swaptionengine.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::g2swaptionengine(py::module_& m) {
    py::class_<G2SwaptionEngine, PricingEngine, ext::shared_ptr<G2SwaptionEngine>>(
        m, "G2SwaptionEngine",
        "Swaption engine for two-factor G2++ model.")
        .def(py::init<const ext::shared_ptr<G2>&, Real, Size>(),
            py::arg("model"),
            py::arg("range"),
            py::arg("intervals"),
            "Constructs G2 swaption engine with integration parameters.");
}
