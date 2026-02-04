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
#include <ql/math/interpolations/cubicinterpolation.hpp>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::cubicinterpolation(py::module_& m) {
    // Enums
    py::enum_<CubicInterpolation::DerivativeApprox>(m, "CubicDerivativeApprox",
        "Derivative approximation methods for cubic interpolation.")
        .value("Spline", CubicInterpolation::Spline)
        .value("SplineOM1", CubicInterpolation::SplineOM1)
        .value("SplineOM2", CubicInterpolation::SplineOM2)
        .value("FourthOrder", CubicInterpolation::FourthOrder)
        .value("Parabolic", CubicInterpolation::Parabolic)
        .value("FritschButland", CubicInterpolation::FritschButland)
        .value("Akima", CubicInterpolation::Akima)
        .value("Kruger", CubicInterpolation::Kruger)
        .value("Harmonic", CubicInterpolation::Harmonic)
        .export_values();

    py::enum_<CubicInterpolation::BoundaryCondition>(m, "CubicBoundaryCondition",
        "Boundary conditions for cubic interpolation.")
        .value("NotAKnot", CubicInterpolation::NotAKnot)
        .value("FirstDerivative", CubicInterpolation::FirstDerivative)
        .value("SecondDerivative", CubicInterpolation::SecondDerivative)
        .value("Periodic", CubicInterpolation::Periodic)
        .value("Lagrange", CubicInterpolation::Lagrange)
        .export_values();

    // CubicInterpolation - uses variadic helper for extra arguments
    py::class_<CubicInterpolation, Interpolation, ext::shared_ptr<CubicInterpolation>>(
        m, "CubicInterpolation",
        "Cubic interpolation between discrete points.")
        .def(py::init([](std::vector<Real> x, std::vector<Real> y,
                        CubicInterpolation::DerivativeApprox da,
                        bool monotonic,
                        CubicInterpolation::BoundaryCondition leftCond,
                        Real leftConditionValue,
                        CubicInterpolation::BoundaryCondition rightCond,
                        Real rightConditionValue) {
            return pyquantlib::make_safe_interpolation<CubicInterpolation>(
                std::move(x), std::move(y), 2,
                da, monotonic, leftCond, leftConditionValue,
                rightCond, rightConditionValue);
        }),
        py::arg("x"), py::arg("y"),
        py::arg("derivativeApprox") = CubicInterpolation::Kruger,
        py::arg("monotonic") = false,
        py::arg("leftCondition") = CubicInterpolation::SecondDerivative,
        py::arg("leftConditionValue") = 0.0,
        py::arg("rightCondition") = CubicInterpolation::SecondDerivative,
        py::arg("rightConditionValue") = 0.0,
        "Constructs cubic interpolation from x and y arrays.");

    // Convenience classes - use simple binding helper
    pyquantlib::bind_simple_interpolation<CubicNaturalSpline>(
        m, "CubicNaturalSpline",
        "Natural cubic spline interpolation.");

    pyquantlib::bind_simple_interpolation<MonotonicCubicNaturalSpline>(
        m, "MonotonicCubicNaturalSpline",
        "Monotonic natural cubic spline interpolation.");
}
