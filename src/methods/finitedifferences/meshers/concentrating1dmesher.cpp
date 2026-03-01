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
#include <ql/methods/finitedifferences/meshers/concentrating1dmesher.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::concentrating1dmesher(py::module_& m) {
    py::class_<Concentrating1dMesher, Fdm1dMesher,
               ext::shared_ptr<Concentrating1dMesher>>(
        m, "Concentrating1dMesher",
        "One-dimensional mesher concentrating around critical points.")
        // Overload 1: single concentration point pair
        .def(py::init([](Real start, Real end, Size size,
                         const py::object& cPoint,
                         bool requireCPoint) {
            const Real nr = Null<Real>();
            std::pair<Real, Real> cp(nr, nr);
            if (!cPoint.is_none())
                cp = cPoint.cast<std::pair<Real, Real>>();
            return ext::make_shared<Concentrating1dMesher>(
                start, end, size, cp, requireCPoint);
        }),
            py::arg("start"), py::arg("end"), py::arg("size"),
            py::arg("cPoint") = py::none(),
            py::arg("requireCPoint") = false,
            "Constructs with optional concentration point (location, density).")
        // Overload 2: multiple concentration points
        .def(py::init<Real, Real, Size,
                       const std::vector<std::tuple<Real, Real, bool>>&,
                       Real>(),
            py::arg("start"), py::arg("end"), py::arg("size"),
            py::arg("cPoints"),
            py::arg("tol") = 1e-8,
            "Constructs with multiple concentration points.");
}
