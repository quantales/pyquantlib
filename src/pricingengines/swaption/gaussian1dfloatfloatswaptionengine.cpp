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
#include <ql/pricingengines/swaption/gaussian1dfloatfloatswaptionengine.hpp>
#include <ql/models/shortrate/onefactormodels/gaussian1dmodel.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::gaussian1dfloatfloatswaptionengine(py::module_& m) {
    auto engine = py::class_<Gaussian1dFloatFloatSwaptionEngine,
               ext::shared_ptr<Gaussian1dFloatFloatSwaptionEngine>,
               PricingEngine>(
        m, "Gaussian1dFloatFloatSwaptionEngine",
        "Gaussian 1-D engine for float-float swaptions.");

    // Probabilities enum
    py::enum_<Gaussian1dFloatFloatSwaptionEngine::Probabilities>(
        engine, "Probabilities",
        "Probability adjustment type.")
        .value("None_", Gaussian1dFloatFloatSwaptionEngine::None)
        .value("Naive", Gaussian1dFloatFloatSwaptionEngine::Naive)
        .value("Digital", Gaussian1dFloatFloatSwaptionEngine::Digital)
        .export_values();

    engine
        .def(py::init<const ext::shared_ptr<Gaussian1dModel>&,
                      int, Real, bool, bool,
                      const Handle<Quote>&,
                      const Handle<YieldTermStructure>&,
                      bool,
                      Gaussian1dFloatFloatSwaptionEngine::Probabilities>(),
            py::arg("model"),
            py::arg("integrationPoints") = 64,
            py::arg("stddevs") = 7.0,
            py::arg("extrapolatePayoff") = true,
            py::arg("flatPayoffExtrapolation") = false,
            py::arg("oas") = Handle<Quote>(),
            py::arg("discountCurve") = Handle<YieldTermStructure>(),
            py::arg("includeTodaysExercise") = false,
            py::arg("probabilities") = Gaussian1dFloatFloatSwaptionEngine::None,
            "Constructs Gaussian 1-D float-float swaption engine.");
}
