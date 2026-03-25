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

void ql_math::loginterpolation(py::module_& m) {
    // LogCubicInterpolation - full constructor
    py::class_<LogCubicInterpolation, Interpolation,
               ext::shared_ptr<LogCubicInterpolation>>(
        m, "LogCubicInterpolation",
        "Log-cubic interpolation between discrete points.")
        .def(py::init([](std::vector<Real> x, std::vector<Real> y,
                        CubicInterpolation::DerivativeApprox da,
                        bool monotonic,
                        CubicInterpolation::BoundaryCondition leftCond,
                        Real leftConditionValue,
                        CubicInterpolation::BoundaryCondition rightCond,
                        Real rightConditionValue) {
            return pyquantlib::make_safe_interpolation<LogCubicInterpolation>(
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
        "Constructs log-cubic interpolation from x and y arrays.");

    // LogCubic convenience classes (simple x, y constructors)
    pyquantlib::bind_simple_interpolation<LogCubicNaturalSpline>(
        m, "LogCubicNaturalSpline",
        "Log-cubic natural spline interpolation.");

    pyquantlib::bind_simple_interpolation<MonotonicLogCubicNaturalSpline>(
        m, "MonotonicLogCubicNaturalSpline",
        "Monotonic log-cubic natural spline interpolation.");

    pyquantlib::bind_simple_interpolation<KrugerLogCubic>(
        m, "KrugerLogCubic",
        "Kruger log-cubic interpolation.");

    pyquantlib::bind_simple_interpolation<HarmonicLogCubic>(
        m, "HarmonicLogCubic",
        "Harmonic log-cubic interpolation.");

    pyquantlib::bind_simple_interpolation<FritschButlandLogCubic>(
        m, "FritschButlandLogCubic",
        "Fritsch-Butland log-cubic interpolation.");

    // LogMixedLinearCubicInterpolation - full constructor
    py::class_<LogMixedLinearCubicInterpolation, Interpolation,
               ext::shared_ptr<LogMixedLinearCubicInterpolation>>(
        m, "LogMixedLinearCubicInterpolation",
        "Log-mixed linear/cubic interpolation between discrete points.")
        .def(py::init([](std::vector<Real> x, std::vector<Real> y,
                        Size n,
                        MixedInterpolation::Behavior behavior,
                        CubicInterpolation::DerivativeApprox da,
                        bool monotonic,
                        CubicInterpolation::BoundaryCondition leftCond,
                        Real leftConditionValue,
                        CubicInterpolation::BoundaryCondition rightCond,
                        Real rightConditionValue) {
            return pyquantlib::make_safe_interpolation<LogMixedLinearCubicInterpolation>(
                std::move(x), std::move(y), 3,
                n, behavior, da, monotonic,
                leftCond, leftConditionValue,
                rightCond, rightConditionValue);
        }),
        py::arg("x"), py::arg("y"),
        py::arg("n"),
        py::arg("behavior") = MixedInterpolation::ShareRanges,
        py::arg("derivativeApprox") = CubicInterpolation::Kruger,
        py::arg("monotonic") = false,
        py::arg("leftCondition") = CubicInterpolation::SecondDerivative,
        py::arg("leftConditionValue") = 0.0,
        py::arg("rightCondition") = CubicInterpolation::SecondDerivative,
        py::arg("rightConditionValue") = 0.0,
        "Constructs log-mixed linear/cubic interpolation.");

    // LogMixedLinearCubicNaturalSpline convenience class
    py::class_<LogMixedLinearCubicNaturalSpline, LogMixedLinearCubicInterpolation,
               ext::shared_ptr<LogMixedLinearCubicNaturalSpline>>(
        m, "LogMixedLinearCubicNaturalSpline",
        "Log-mixed linear/natural cubic spline interpolation.")
        .def(py::init([](std::vector<Real> x, std::vector<Real> y,
                        Size n,
                        MixedInterpolation::Behavior behavior) {
            return pyquantlib::make_safe_interpolation<LogMixedLinearCubicNaturalSpline>(
                std::move(x), std::move(y), 3,
                n, behavior);
        }),
        py::arg("x"), py::arg("y"),
        py::arg("n"),
        py::arg("behavior") = MixedInterpolation::ShareRanges,
        "Constructs interpolation from x and y arrays.");
}
