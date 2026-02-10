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
#include <ql/termstructures/volatility/swaption/swaptionvoldiscrete.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::swaptionvoldiscrete(py::module_& m) {
    // SwaptionVolatilityDiscrete is an intermediate class that combines
    // LazyObject + SwaptionVolatilityStructure (diamond through Observable).
    // Uses py::classh for diamond inheritance.
    py::classh<SwaptionVolatilityDiscrete,
               LazyObject, SwaptionVolatilityStructure>(
        m, "SwaptionVolatilityDiscrete",
        "Intermediate class for discrete swaption volatility structures.")
        // No constructors exposed (abstract intermediate class)
        .def("optionTenors", &SwaptionVolatilityDiscrete::optionTenors,
            "Returns the option tenors.")
        .def("optionDates", &SwaptionVolatilityDiscrete::optionDates,
            "Returns the option dates.")
        .def("optionTimes", &SwaptionVolatilityDiscrete::optionTimes,
            "Returns the option times.")
        .def("swapTenors", &SwaptionVolatilityDiscrete::swapTenors,
            "Returns the swap tenors.")
        .def("swapLengths", &SwaptionVolatilityDiscrete::swapLengths,
            "Returns the swap lengths.");
}
