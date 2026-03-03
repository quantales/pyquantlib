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
#include <ql/math/interpolations/bicubicsplineinterpolation.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>

namespace py = pybind11;
using namespace QuantLib;

namespace {

struct BicubicDataHolder {
    std::vector<Real> x, y;
    ext::shared_ptr<Matrix> z;

    void operator()(BicubicSpline* p) const { delete p; }
};

} // anonymous namespace

void ql_math::bicubicsplineinterpolation(py::module_& m) {
    py::class_<BicubicSpline, Interpolation2D,
               ext::shared_ptr<BicubicSpline>>(
        m, "BicubicSpline",
        "Bicubic spline interpolation on a 2-D grid.")
        .def(py::init([](std::vector<Real> x, std::vector<Real> y,
                         const Matrix& z) {
            QL_REQUIRE(x.size() >= 2 && y.size() >= 2,
                       "at least 2 points required in each dimension");
            QL_REQUIRE(z.rows() == y.size() && z.columns() == x.size(),
                       "z matrix dimensions must match: "
                       "rows = y.size(), columns = x.size()");

            auto zPtr = ext::make_shared<Matrix>(z);
            BicubicDataHolder holder{std::move(x), std::move(y), zPtr};
            auto* ptr = new BicubicSpline(
                holder.x.begin(), holder.x.end(),
                holder.y.begin(), holder.y.end(),
                *holder.z);
            return ext::shared_ptr<BicubicSpline>(ptr, std::move(holder));
        }),
        py::arg("x"), py::arg("y"), py::arg("z"),
        "Constructs from x, y arrays and z matrix.")
        .def("derivativeX", &BicubicSpline::derivativeX,
            py::arg("x"), py::arg("y"),
            "Returns the partial derivative with respect to x.")
        .def("derivativeY", &BicubicSpline::derivativeY,
            py::arg("x"), py::arg("y"),
            "Returns the partial derivative with respect to y.")
        .def("secondDerivativeX", &BicubicSpline::secondDerivativeX,
            py::arg("x"), py::arg("y"),
            "Returns the second partial derivative with respect to x.")
        .def("secondDerivativeY", &BicubicSpline::secondDerivativeY,
            py::arg("x"), py::arg("y"),
            "Returns the second partial derivative with respect to y.")
        .def("derivativeXY", &BicubicSpline::derivativeXY,
            py::arg("x"), py::arg("y"),
            "Returns the cross partial derivative.");
}
