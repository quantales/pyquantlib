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
#include <ql/math/interpolations/lagrangeinterpolation.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>

namespace py = pybind11;
using namespace QuantLib;

namespace {

// Data holder that owns x and y vectors for safe iterator lifetime.
struct LagrangeDataHolder {
    std::vector<Real> x, y;

    void operator()(LagrangeInterpolation* p) const { delete p; }
};

} // anonymous namespace

void ql_math::lagrangeinterpolation(py::module_& m) {
    py::class_<LagrangeInterpolation, Interpolation,
               ext::shared_ptr<LagrangeInterpolation>>(
        m, "LagrangeInterpolation",
        "Lagrange interpolation through discrete points.")
        .def(py::init([](std::vector<Real> x, std::vector<Real> y) {
            QL_REQUIRE(x.size() == y.size(),
                       "x and y must have the same size");
            QL_REQUIRE(x.size() >= 2, "at least 2 points required");

            LagrangeDataHolder holder{std::move(x), std::move(y)};
            auto* ptr = new LagrangeInterpolation(
                holder.x.begin(), holder.x.end(), holder.y.begin());
            return ext::shared_ptr<LagrangeInterpolation>(
                ptr, std::move(holder));
        }),
        py::arg("x"), py::arg("y"),
        "Constructs interpolation from x and y arrays.")
        .def("value", &LagrangeInterpolation::value,
            py::arg("y"), py::arg("x"),
            "Evaluates at x using alternative y values.");
}
