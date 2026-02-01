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
#include <ql/pricingengines/swaption/jamshidianswaptionengine.hpp>
#include <ql/models/shortrate/onefactormodel.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::jamshidianswaptionengine(py::module_& m) {
    py::class_<JamshidianSwaptionEngine, PricingEngine,
               ext::shared_ptr<JamshidianSwaptionEngine>>(
        m, "JamshidianSwaptionEngine",
        "Jamshidian swaption engine using bond option decomposition.")
        // Constructor with handle
        .def(py::init<const ext::shared_ptr<OneFactorAffineModel>&,
                      Handle<YieldTermStructure>>(),
            py::arg("model"),
            py::arg("termStructure") = Handle<YieldTermStructure>(),
            "Constructs Jamshidian engine with one-factor affine model.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<OneFactorAffineModel>& model,
                        const ext::shared_ptr<YieldTermStructure>& ts) {
            return ext::make_shared<JamshidianSwaptionEngine>(
                model,
                ts ? Handle<YieldTermStructure>(ts) : Handle<YieldTermStructure>());
        }),
            py::arg("model"),
            py::arg("termStructure"),
            "Constructs Jamshidian engine with model and term structure.");
}
