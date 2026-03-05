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
#include <ql/termstructures/volatility/swaption/spreadedswaptionvol.hpp>
#include <ql/termstructures/volatility/swaption/swaptionvolstructure.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::spreadedswaptionvolatility(py::module_& m) {
    py::class_<SpreadedSwaptionVolatility, SwaptionVolatilityStructure,
               ext::shared_ptr<SpreadedSwaptionVolatility>>(
        m, "SpreadedSwaptionVolatility",
        "Swaption volatility with an additive spread.")
        // Handle constructor
        .def(py::init<const Handle<SwaptionVolatilityStructure>&,
                      Handle<Quote>>(),
            py::arg("baseVolHandle"), py::arg("spreadHandle"),
            "Constructs from swaption vol and spread handles.")
        // Hidden handle
        .def(py::init([](const ext::shared_ptr<SwaptionVolatilityStructure>& vol,
                         const ext::shared_ptr<Quote>& spread) {
            return ext::make_shared<SpreadedSwaptionVolatility>(
                Handle<SwaptionVolatilityStructure>(vol),
                Handle<Quote>(spread));
        }),
            py::arg("baseVol"), py::arg("spread"),
            "Constructs from shared_ptrs (handles created internally).");
}
