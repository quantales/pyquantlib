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
#include <ql/pricingengines/capfloor/analyticcapfloorengine.hpp>
#include <ql/models/model.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::analyticcapfloorengine(py::module_& m) {
    py::class_<AnalyticCapFloorEngine,
               ext::shared_ptr<AnalyticCapFloorEngine>,
               PricingEngine>(
        m, "AnalyticCapFloorEngine",
        "Analytic cap/floor engine for affine short-rate models.")
        .def(py::init<const ext::shared_ptr<AffineModel>&,
                      Handle<YieldTermStructure>>(),
            py::arg("model"),
            py::arg("termStructure") = Handle<YieldTermStructure>(),
            "Constructs analytic cap/floor engine.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<AffineModel>& model,
                         const ext::shared_ptr<YieldTermStructure>& ts) {
            return ext::make_shared<AnalyticCapFloorEngine>(
                model,
                ts ? Handle<YieldTermStructure>(ts)
                   : Handle<YieldTermStructure>());
        }),
            py::arg("model"),
            py::arg("termStructure"),
            "Constructs analytic cap/floor engine (handle created internally).");
}
