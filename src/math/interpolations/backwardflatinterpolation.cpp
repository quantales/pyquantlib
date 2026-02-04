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
#include "pyquantlib/interpolation_helper.h"
#include <ql/math/interpolations/backwardflatinterpolation.hpp>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::backwardflatinterpolation(py::module_& m) {
    // BackwardFlatInterpolation only requires 1 point
    pyquantlib::bind_simple_interpolation<BackwardFlatInterpolation, 1>(
        m, "BackwardFlatInterpolation",
        "Backward-flat interpolation between discrete points.");
}
