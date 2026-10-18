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
#include <ql/termstructures/volatility/equityfx/localvolcurve.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::localvolcurve(py::module_& m) {
    py::class_<LocalVolCurve, LocalVolTermStructure,
               ext::shared_ptr<LocalVolCurve>>(
        m, "LocalVolCurve",
        "Local volatility curve derived from a Black variance curve.")
        .def(py::init([](const ext::shared_ptr<BlackVarianceCurve>& curve) {
            return ext::make_shared<LocalVolCurve>(Handle<BlackVarianceCurve>(curve));
        }),
            py::arg("curve"),
            "Constructs from a Black variance curve (handle created internally).")
        .def("maxDate", &LocalVolCurve::maxDate,
            "Returns the maximum date.")
        .def("minStrike", &LocalVolCurve::minStrike,
            "Returns the minimum strike.")
        .def("maxStrike", &LocalVolCurve::maxStrike,
            "Returns the maximum strike.");
}
