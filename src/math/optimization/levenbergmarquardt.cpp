/*
 * PyQuantLib: Python bindings for QuantLib
 * Copyright (c) 2025 Yassine Idyiahia
 * 
 * QuantLib is Copyright (c) 2000-2025 The QuantLib Authors
 * QuantLib is free software under a modified BSD license.
 * See http://quantlib.org/ for more information.
 * 
 * Source: https://github.com/quantales/pyquantlib
 * Licensed under the BSD 3-Clause License. See LICENSE file for details.
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/math/optimization/levenbergmarquardt.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::levenbergmarquardt(py::module_& m) {
    py::class_<LevenbergMarquardt, OptimizationMethod, ext::shared_ptr<LevenbergMarquardt>>(
        m, "LevenbergMarquardt",
        "Levenberg-Marquardt optimization method.")
        .def(py::init<Real, Real, Real>(),
            py::arg("epsfcn") = 1.0e-8,
            py::arg("xtol") = 1.0e-8,
            py::arg("gtol") = 1.0e-8,
            "Creates a Levenberg-Marquardt optimizer.");
}
