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
#include <ql/termstructures/volatility/swaption/swaptionvolcube.hpp>
#include <ql/termstructures/volatility/swaption/swaptionvolstructure.hpp>
#include <ql/indexes/swapindex.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::swaptionvolcube(py::module_& m) {
    py::class_<SwaptionVolatilityCube, SwaptionVolatilityDiscrete,
               ext::shared_ptr<SwaptionVolatilityCube>>(
        m, "SwaptionVolatilityCube",
        "Abstract base for swaption volatility cubes with smile.")
        // No constructors: SwaptionVolatilityCube is abstract
        // (smileSectionImpl not overridden). Use SabrSwaptionVolatilityCube.
        .def("atmStrike",
            py::overload_cast<const Date&, const Period&>(
                &SwaptionVolatilityCube::atmStrike, py::const_),
            py::arg("optionDate"), py::arg("swapTenor"),
            "Returns ATM strike for option date and swap tenor.")
        .def("atmStrike",
            py::overload_cast<const Period&, const Period&>(
                &SwaptionVolatilityCube::atmStrike, py::const_),
            py::arg("optionTenor"), py::arg("swapTenor"),
            "Returns ATM strike for option tenor and swap tenor.")
        .def("atmVol", &SwaptionVolatilityCube::atmVol,
            "Returns the ATM volatility structure handle.")
        .def("strikeSpreads", &SwaptionVolatilityCube::strikeSpreads,
            "Returns the strike spreads.")
        .def("volSpreads", &SwaptionVolatilityCube::volSpreads,
            "Returns the volatility spread handles.")
        .def("swapIndexBase", &SwaptionVolatilityCube::swapIndexBase,
            "Returns the swap index base.")
        .def("shortSwapIndexBase", &SwaptionVolatilityCube::shortSwapIndexBase,
            "Returns the short swap index base.")
        .def("vegaWeightedSmileFit", &SwaptionVolatilityCube::vegaWeightedSmileFit,
            "Returns whether smile fit is vega-weighted.");
}
