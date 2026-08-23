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
#include <ql/termstructures/volatility/equityfx/andreasenhugevolatilityadapter.hpp>
#include <ql/termstructures/volatility/equityfx/andreasenhugevolatilityinterpl.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::andreasenhugevolatilityadapter(py::module_& m) {
    py::class_<AndreasenHugeVolatilityAdapter, BlackVolTermStructure,
               ext::shared_ptr<AndreasenHugeVolatilityAdapter>>(
        m, "AndreasenHugeVolatilityAdapter",
        "BlackVolTermStructure adapter for Andreasen-Huge volatility "
        "interpolation. Provides implied Black volatility.")
        .def(py::init<ext::shared_ptr<AndreasenHugeVolatilityInterpl>, Real>(),
            py::arg("volInterpl"),
            py::arg("eps") = 1e-6,
            "Constructs from an AndreasenHugeVolatilityInterpl instance.");
}
