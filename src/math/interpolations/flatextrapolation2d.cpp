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
#include <ql/math/interpolations/flatextrapolation2d.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::flatextrapolation2d(py::module_& m) {
    py::class_<FlatExtrapolator2D, Interpolation2D,
               ext::shared_ptr<FlatExtrapolator2D>>(
        m, "FlatExtrapolator2D",
        "2-D flat extrapolation decorator.")
        .def(py::init<const ext::shared_ptr<Interpolation2D>&>(),
            py::arg("interpolation"),
            "Constructs flat extrapolator wrapping a 2-D interpolation.");
}
