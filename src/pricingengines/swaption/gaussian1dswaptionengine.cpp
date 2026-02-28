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
#include <ql/pricingengines/swaption/gaussian1dswaptionengine.hpp>
#include <ql/models/shortrate/onefactormodels/gaussian1dmodel.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::gaussian1dswaptionengine(py::module_& m) {
    auto engine = py::class_<Gaussian1dSwaptionEngine,
               ext::shared_ptr<Gaussian1dSwaptionEngine>,
               PricingEngine>(
        m, "Gaussian1dSwaptionEngine",
        "Gaussian 1-D swaption engine for Bermudan/European swaptions.");

    // Probabilities enum
    py::enum_<Gaussian1dSwaptionEngine::Probabilities>(engine, "Probabilities",
        "Probability adjustment type.")
        .value("None_", Gaussian1dSwaptionEngine::None)
        .value("Naive", Gaussian1dSwaptionEngine::Naive)
        .value("Digital", Gaussian1dSwaptionEngine::Digital)
        .export_values();

    engine
        // Constructor from shared_ptr
        .def(py::init<const ext::shared_ptr<Gaussian1dModel>&,
                      int, Real, bool, bool,
                      Handle<YieldTermStructure>,
                      Gaussian1dSwaptionEngine::Probabilities>(),
            py::arg("model"),
            py::arg("integrationPoints") = 64,
            py::arg("stddevs") = 7.0,
            py::arg("extrapolatePayoff") = true,
            py::arg("flatPayoffExtrapolation") = false,
            py::arg("discountCurve") = Handle<YieldTermStructure>(),
            py::arg("probabilities") = Gaussian1dSwaptionEngine::None,
            "Constructs Gaussian 1-D swaption engine.");
}
