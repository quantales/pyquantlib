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
#include <ql/math/interpolations/flatextrapolation.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::flatextrapolation(py::module_& m) {
    py::class_<FlatExtrapolator, Interpolation,
               ext::shared_ptr<FlatExtrapolator>>(
        m, "FlatExtrapolator",
        "1-D flat extrapolation decorator.")
        .def(py::init<const ext::shared_ptr<Interpolation>&>(),
            py::arg("interpolation"),
            "Constructs flat extrapolator wrapping a 1-D interpolation.");
}
