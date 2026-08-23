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
#include <ql/termstructures/volatility/equityfx/andreasenhugelocalvoladapter.hpp>
#include <ql/termstructures/volatility/equityfx/andreasenhugevolatilityinterpl.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::andreasenhugelocalvoladapter(py::module_& m) {
    py::class_<AndreasenHugeLocalVolAdapter, LocalVolTermStructure,
               ext::shared_ptr<AndreasenHugeLocalVolAdapter>>(
        m, "AndreasenHugeLocalVolAdapter",
        "LocalVolTermStructure adapter for Andreasen-Huge volatility "
        "interpolation.")
        .def(py::init<ext::shared_ptr<AndreasenHugeVolatilityInterpl>>(),
            py::arg("localVol"),
            "Constructs from an AndreasenHugeVolatilityInterpl instance.");
}
