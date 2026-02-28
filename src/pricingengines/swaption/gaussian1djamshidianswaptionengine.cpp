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
#include <ql/pricingengines/swaption/gaussian1djamshidianswaptionengine.hpp>
#include <ql/models/shortrate/onefactormodels/gaussian1dmodel.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::gaussian1djamshidianswaptionengine(py::module_& m) {
    py::class_<Gaussian1dJamshidianSwaptionEngine,
               ext::shared_ptr<Gaussian1dJamshidianSwaptionEngine>,
               PricingEngine>(
        m, "Gaussian1dJamshidianSwaptionEngine",
        "Gaussian 1-D Jamshidian swaption engine (analytic decomposition).")
        .def(py::init<const ext::shared_ptr<Gaussian1dModel>&>(),
            py::arg("model"),
            "Constructs Jamshidian swaption engine.");
}
