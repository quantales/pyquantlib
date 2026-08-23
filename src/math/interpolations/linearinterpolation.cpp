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
#include "pyquantlib/interpolation_helper.h"
#include <ql/math/interpolations/linearinterpolation.hpp>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::linearinterpolation(py::module_& m) {
    pyquantlib::bind_simple_interpolation<LinearInterpolation>(
        m, "LinearInterpolation",
        "Linear interpolation between discrete points.");
}
