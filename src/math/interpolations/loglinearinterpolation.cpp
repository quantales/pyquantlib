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
#include <ql/math/interpolations/loginterpolation.hpp>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::loglinearinterpolation(py::module_& m) {
    pyquantlib::bind_simple_interpolation<LogLinearInterpolation>(
        m, "LogLinearInterpolation",
        "Log-linear interpolation between discrete points.");
}
