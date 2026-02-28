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
#include <ql/pricingengines/vanilla/analyticbsmhullwhiteengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/models/shortrate/onefactormodels/hullwhite.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::analyticbsmhullwhiteengine(py::module_& m) {
    py::class_<AnalyticBSMHullWhiteEngine,
               ext::shared_ptr<AnalyticBSMHullWhiteEngine>,
               PricingEngine>(
        m, "AnalyticBSMHullWhiteEngine",
        "BSM engine with Hull-White stochastic interest rates.")
        .def(py::init<Real,
                      const ext::shared_ptr<GeneralizedBlackScholesProcess>&,
                      const ext::shared_ptr<HullWhite>&>(),
            py::arg("equityShortRateCorrelation"),
            py::arg("process"),
            py::arg("hullWhiteModel"),
            "Constructs BSM Hull-White engine.");
}
