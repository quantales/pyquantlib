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
#include <ql/pricingengines/bond/discountingbondengine.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::discountingbondengine(py::module_& m) {
    py::class_<DiscountingBondEngine, Bond::engine,
        ext::shared_ptr<DiscountingBondEngine>>(
        m, "DiscountingBondEngine",
        "Discounting engine for bonds.")
        // Constructor with handle
        .def(py::init<Handle<YieldTermStructure>,
                      const ext::optional<bool>&>(),
            py::arg("discountCurve") = Handle<YieldTermStructure>(),
            py::arg("includeSettlementDateFlows") = ext::nullopt,
            "Constructs discounting bond engine.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& discountCurve,
                        const ext::optional<bool>& includeSettlementDateFlows) {
            return ext::make_shared<DiscountingBondEngine>(
                Handle<YieldTermStructure>(discountCurve),
                includeSettlementDateFlows);
        }),
            py::arg("discountCurve"),
            py::arg("includeSettlementDateFlows") = ext::nullopt,
            "Constructs discounting bond engine from term structure.")
        .def("discountCurve", &DiscountingBondEngine::discountCurve,
            "Returns the discount curve handle.");
}
