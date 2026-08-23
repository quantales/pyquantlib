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
#include <ql/termstructures/volatility/optionlet/strippedoptionletadapter.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::strippedoptionletadapter(py::module_& m) {
    // Diamond: OptionletVolatilityStructure + LazyObject (both through Observable)
    py::classh<StrippedOptionletAdapter,
               OptionletVolatilityStructure, LazyObject>(
        m, "StrippedOptionletAdapter",
        "Adapts stripped optionlet data into an OptionletVolatilityStructure.")
        .def(py::init<const ext::shared_ptr<StrippedOptionletBase>&>(),
            py::arg("optionletStripper"),
            "Constructs from a StrippedOptionletBase.")
        .def("maxDate", &StrippedOptionletAdapter::maxDate,
            "Returns the maximum date.")
        .def("minStrike", &StrippedOptionletAdapter::minStrike,
            "Returns the minimum strike.")
        .def("maxStrike", &StrippedOptionletAdapter::maxStrike,
            "Returns the maximum strike.")
        .def("volatilityType", &StrippedOptionletAdapter::volatilityType,
            "Returns the volatility type.")
        .def("displacement", &StrippedOptionletAdapter::displacement,
            "Returns the displacement for shifted lognormal volatilities.");
}
