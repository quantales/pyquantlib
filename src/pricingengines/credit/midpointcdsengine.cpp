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
#include <ql/pricingengines/credit/midpointcdsengine.hpp>
#include <ql/termstructures/defaulttermstructure.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::midpointcdsengine(py::module_& m) {
    py::class_<MidPointCdsEngine, PricingEngine,
               ext::shared_ptr<MidPointCdsEngine>>(
        m, "MidPointCdsEngine",
        "Mid-point engine for credit default swaps.")
        // Handle constructor
        .def(py::init<Handle<DefaultProbabilityTermStructure>,
                       Real, Handle<YieldTermStructure>,
                       const ext::optional<bool>&>(),
            py::arg("probability"),
            py::arg("recoveryRate"),
            py::arg("discountCurve"),
            py::arg("includeSettlementDateFlows") = ext::nullopt,
            "Constructs from handles.")
        // Hidden handle: shared_ptr convenience
        .def(py::init([](const ext::shared_ptr<DefaultProbabilityTermStructure>& prob,
                         Real recoveryRate,
                         const ext::shared_ptr<YieldTermStructure>& disc,
                         const ext::optional<bool>& settle) {
            return ext::make_shared<MidPointCdsEngine>(
                Handle<DefaultProbabilityTermStructure>(prob),
                recoveryRate,
                Handle<YieldTermStructure>(disc),
                settle);
        }),
            py::arg("probability"),
            py::arg("recoveryRate"),
            py::arg("discountCurve"),
            py::arg("includeSettlementDateFlows") = ext::nullopt,
            "Constructs from term structures (handles created internally).");
}
