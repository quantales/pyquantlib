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
#include <ql/math/interpolations/convexmonotoneinterpolation.hpp>

namespace py = pybind11;
using namespace QuantLib;

// Concrete instantiation for vector iterators
using ConvexMonotoneInterp = ConvexMonotoneInterpolation<
    std::vector<Real>::iterator, std::vector<Real>::iterator>;

void ql_math::convexmonotoneinterpolation(py::module_& m) {
    py::class_<ConvexMonotoneInterp, Interpolation,
               ext::shared_ptr<ConvexMonotoneInterp>>(
        m, "ConvexMonotoneInterpolation",
        "Convex monotone yield-curve interpolation (Hagan & West, 2006).")
        .def(py::init([](std::vector<Real> x, std::vector<Real> y,
                        Real quadraticity, Real monotonicity,
                        bool forcePositive, bool flatFinalPeriod) {
            QL_REQUIRE(x.size() == y.size(),
                       "x and y must have the same size");
            QL_REQUIRE(x.size() >= 2, "at least 2 points required");

            pyquantlib::detail::InterpolationDataHolder holder{
                std::move(x), std::move(y)};

            auto* ptr = new ConvexMonotoneInterp(
                holder.x.begin(), holder.x.end(), holder.y.begin(),
                quadraticity, monotonicity, forcePositive, flatFinalPeriod);

            return ext::shared_ptr<ConvexMonotoneInterp>(
                ptr, std::move(holder));
        }),
        py::arg("x"), py::arg("y"),
        py::arg("quadraticity") = 0.3,
        py::arg("monotonicity") = 0.7,
        py::arg("forcePositive") = true,
        py::arg("flatFinalPeriod") = false,
        "Constructs convex monotone interpolation.");
}
