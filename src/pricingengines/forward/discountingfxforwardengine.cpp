/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2026 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is Copyright (c) 2000-2026 The QuantLib Authors
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/pricingengines/forward/discountingfxforwardengine.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::discountingfxforwardengine(py::module_& m) {
    py::class_<DiscountingFxForwardEngine, PricingEngine,
               ext::shared_ptr<DiscountingFxForwardEngine>>(
        m, "DiscountingFxForwardEngine",
        "Discounts the two legs of an FX forward using their currency curves.")
        // Explicit handles
        .def(py::init<Handle<YieldTermStructure>, Handle<YieldTermStructure>,
                      Handle<Quote>>(),
            py::arg("sourceCurrencyDiscountCurve"),
            py::arg("targetCurrencyDiscountCurve"),
            py::arg("spotFx"),
            "Constructs from source/target discount curves and the spot FX quote "
            "(target per unit of source).")
        // Hidden handles
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& sourceCurve,
                         const ext::shared_ptr<YieldTermStructure>& targetCurve,
                         const ext::shared_ptr<Quote>& spotFx) {
            return ext::make_shared<DiscountingFxForwardEngine>(
                Handle<YieldTermStructure>(sourceCurve),
                Handle<YieldTermStructure>(targetCurve),
                Handle<Quote>(spotFx));
        }),
            py::arg("sourceCurrencyDiscountCurve"),
            py::arg("targetCurrencyDiscountCurve"),
            py::arg("spotFx"),
            "Constructs from curves and spot quote (handles created internally).")
        // Inspectors
        .def("sourceCurrencyDiscountCurve",
            &DiscountingFxForwardEngine::sourceCurrencyDiscountCurve,
            "Returns the source-currency discount curve handle.")
        .def("targetCurrencyDiscountCurve",
            &DiscountingFxForwardEngine::targetCurrencyDiscountCurve,
            "Returns the target-currency discount curve handle.")
        .def("spotFx", &DiscountingFxForwardEngine::spotFx,
            "Returns the spot FX quote handle.");
}
