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
#include <ql/pricingengines/asian/analytic_cont_geom_av_price.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::analyticcontinuousgeometricasianengine(py::module_& m) {
    py::class_<AnalyticContinuousGeometricAveragePriceAsianEngine,
               PricingEngine,
               ext::shared_ptr<AnalyticContinuousGeometricAveragePriceAsianEngine>>(
        m, "AnalyticContinuousGeometricAveragePriceAsianEngine",
        "Analytic continuous geometric average price Asian engine.")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>>(),
            py::arg("process"),
            "Constructs engine.");
}
