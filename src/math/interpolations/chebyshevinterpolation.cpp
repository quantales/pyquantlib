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
#include <ql/math/interpolations/chebyshevinterpolation.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::chebyshevinterpolation(py::module_& m) {
    using CI = ChebyshevInterpolation;

    py::enum_<CI::PointsType>(m, "ChebyshevPointsType",
        "Chebyshev node type.")
        .value("FirstKind", CI::FirstKind)
        .value("SecondKind", CI::SecondKind);

    // ChebyshevInterpolation has deleted copy/move, so construct in-place
    // with make_shared via the two-arg constructor (n, f).
    py::class_<CI, Interpolation, ext::shared_ptr<CI>>(
        m, "ChebyshevInterpolation",
        "Chebyshev interpolation on [-1, 1].")
        .def(py::init([](Size n, const std::function<Real(Real)>& f,
                         CI::PointsType pointsType) {
            return ext::make_shared<CI>(n, f, pointsType);
        }),
        py::arg("n"), py::arg("f"),
        py::arg("pointsType") = CI::SecondKind,
        "Constructs from n points and function f on [-1, 1].")
        .def(py::init([](const Array& y, CI::PointsType pointsType) {
            return ext::make_shared<CI>(y, pointsType);
        }),
        py::arg("y"), py::arg("pointsType") = CI::SecondKind,
        "Constructs from pre-computed y values at Chebyshev nodes.")
        .def("updateY", &CI::updateY,
            py::arg("y"),
            "Updates the y values.")
        .def("nodes", static_cast<Array (CI::*)() const>(&CI::nodes),
            "Returns the Chebyshev nodes.")
        .def_static("nodesStatic",
            static_cast<Array (*)(Size, CI::PointsType)>(&CI::nodes),
            py::arg("n"), py::arg("pointsType"),
            "Returns Chebyshev nodes for given n and type.");
}
