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
#include <ql/pricingengines/swap/discountingswapengine.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::discountingswapengine(py::module_& m) {
    py::class_<DiscountingSwapEngine, Swap::engine,
        ext::shared_ptr<DiscountingSwapEngine>>(
        m, "DiscountingSwapEngine",
        "Discounting engine for swaps.")
        // Constructor with handle
        .def(py::init<Handle<YieldTermStructure>,
                      const ext::optional<bool>&,
                      Date, Date>(),
            py::arg("discountCurve"),
            py::arg("includeSettlementDateFlows") = ext::nullopt,
            py::arg("settlementDate") = Date(),
            py::arg("npvDate") = Date(),
            "Constructs discounting swap engine.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& discountCurve,
                        const ext::optional<bool>& includeSettlementDateFlows,
                        Date settlementDate, Date npvDate) {
            return ext::make_shared<DiscountingSwapEngine>(
                Handle<YieldTermStructure>(discountCurve),
                includeSettlementDateFlows, settlementDate, npvDate);
        }),
            py::arg("discountCurve"),
            py::arg("includeSettlementDateFlows") = ext::nullopt,
            py::arg("settlementDate") = Date(),
            py::arg("npvDate") = Date(),
            "Constructs discounting swap engine from term structure.")
        .def("discountCurve", &DiscountingSwapEngine::discountCurve,
            "Returns the discount curve handle.");
}
