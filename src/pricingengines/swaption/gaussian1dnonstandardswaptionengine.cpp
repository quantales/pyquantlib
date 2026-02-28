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
#include <ql/pricingengines/swaption/gaussian1dnonstandardswaptionengine.hpp>
#include <ql/models/shortrate/onefactormodels/gaussian1dmodel.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::gaussian1dnonstandardswaptionengine(py::module_& m) {
    auto engine = py::class_<Gaussian1dNonstandardSwaptionEngine,
               ext::shared_ptr<Gaussian1dNonstandardSwaptionEngine>,
               PricingEngine>(
        m, "Gaussian1dNonstandardSwaptionEngine",
        "Gaussian 1-D engine for nonstandard swaptions.");

    // Probabilities enum
    py::enum_<Gaussian1dNonstandardSwaptionEngine::Probabilities>(
        engine, "Probabilities",
        "Probability adjustment type.")
        .value("None_", Gaussian1dNonstandardSwaptionEngine::None)
        .value("Naive", Gaussian1dNonstandardSwaptionEngine::Naive)
        .value("Digital", Gaussian1dNonstandardSwaptionEngine::Digital)
        .export_values();

    engine
        .def(py::init<const ext::shared_ptr<Gaussian1dModel>&,
                      int, Real, bool, bool,
                      const Handle<Quote>&,
                      const Handle<YieldTermStructure>&,
                      Gaussian1dNonstandardSwaptionEngine::Probabilities>(),
            py::arg("model"),
            py::arg("integrationPoints") = 64,
            py::arg("stddevs") = 7.0,
            py::arg("extrapolatePayoff") = true,
            py::arg("flatPayoffExtrapolation") = false,
            py::arg("oas") = Handle<Quote>(),
            py::arg("discountCurve") = Handle<YieldTermStructure>(),
            py::arg("probabilities") = Gaussian1dNonstandardSwaptionEngine::None,
            "Constructs Gaussian 1-D nonstandard swaption engine.");
}
