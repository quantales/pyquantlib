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
#include <ql/math/interpolations/mixedinterpolation.hpp>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::mixedinterpolation(py::module_& m) {
    // Enum
    py::enum_<MixedInterpolation::Behavior>(m, "MixedInterpolationBehavior",
        "Behavior for mixed interpolation at the switch point.")
        .value("ShareRanges", MixedInterpolation::ShareRanges)
        .value("SplitRanges", MixedInterpolation::SplitRanges)
        .export_values();

    // MixedLinearCubicInterpolation - full constructor
    py::class_<MixedLinearCubicInterpolation, Interpolation,
               ext::shared_ptr<MixedLinearCubicInterpolation>>(
        m, "MixedLinearCubicInterpolation",
        "Mixed linear/cubic interpolation between discrete points.")
        .def(py::init([](std::vector<Real> x, std::vector<Real> y,
                        Size n,
                        MixedInterpolation::Behavior behavior,
                        CubicInterpolation::DerivativeApprox da,
                        bool monotonic,
                        CubicInterpolation::BoundaryCondition leftCond,
                        Real leftConditionValue,
                        CubicInterpolation::BoundaryCondition rightCond,
                        Real rightConditionValue) {
            return pyquantlib::make_safe_interpolation<MixedLinearCubicInterpolation>(
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
        "Constructs mixed linear/cubic interpolation.");

    // Convenience classes
    auto bind_mixed_convenience = [&](auto* tag, const char* name, const char* doc) {
        using T = std::remove_pointer_t<decltype(tag)>;
        py::class_<T, MixedLinearCubicInterpolation, ext::shared_ptr<T>>(m, name, doc)
            .def(py::init([](std::vector<Real> x, std::vector<Real> y,
                            Size n,
                            MixedInterpolation::Behavior behavior) {
                return pyquantlib::make_safe_interpolation<T>(
                    std::move(x), std::move(y), 3,
                    n, behavior);
            }),
            py::arg("x"), py::arg("y"),
            py::arg("n"),
            py::arg("behavior") = MixedInterpolation::ShareRanges,
            "Constructs interpolation from x and y arrays.");
    };

    bind_mixed_convenience(
        (MixedLinearCubicNaturalSpline*)nullptr,
        "MixedLinearCubicNaturalSpline",
        "Mixed linear/natural cubic spline interpolation.");

    bind_mixed_convenience(
        (MixedLinearMonotonicCubicNaturalSpline*)nullptr,
        "MixedLinearMonotonicCubicNaturalSpline",
        "Mixed linear/monotonic natural cubic spline interpolation.");

    bind_mixed_convenience(
        (MixedLinearKrugerCubic*)nullptr,
        "MixedLinearKrugerCubic",
        "Mixed linear/Kruger cubic interpolation.");

    bind_mixed_convenience(
        (MixedLinearFritschButlandCubic*)nullptr,
        "MixedLinearFritschButlandCubic",
        "Mixed linear/Fritsch-Butland cubic interpolation.");
}
