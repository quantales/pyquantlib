/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/termstructures/volatility/optionlet/spreadedoptionletvol.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::spreadedoptionletvol(py::module_& m) {
    py::class_<SpreadedOptionletVolatility, OptionletVolatilityStructure,
               ext::shared_ptr<SpreadedOptionletVolatility>>(
        m, "SpreadedOptionletVolatility",
        "Optionlet volatility structure shifted by a constant spread.")
        .def(py::init<const Handle<OptionletVolatilityStructure>&, Handle<Quote>>(),
            py::arg("baseVol"), py::arg("spread"),
            "Constructs from a base volatility handle and a spread quote handle.")
        .def(py::init([](const ext::shared_ptr<OptionletVolatilityStructure>& baseVol,
                         const ext::shared_ptr<Quote>& spread) {
            return ext::make_shared<SpreadedOptionletVolatility>(
                Handle<OptionletVolatilityStructure>(baseVol),
                Handle<Quote>(spread));
        }),
            py::arg("baseVol"), py::arg("spread"),
            "Constructs from a base volatility and a spread quote (handles created internally).");
}
