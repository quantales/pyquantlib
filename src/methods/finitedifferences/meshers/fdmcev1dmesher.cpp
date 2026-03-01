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
#include <ql/methods/finitedifferences/meshers/fdmcev1dmesher.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmcev1dmesher(py::module_& m) {
    py::class_<FdmCEV1dMesher, Fdm1dMesher,
               ext::shared_ptr<FdmCEV1dMesher>>(
        m, "FdmCEV1dMesher",
        "One-dimensional mesher for the CEV model.")
        .def(py::init([](Size size, Real f0, Real alpha, Real beta,
                         Time maturity, Real eps, Real scaleFactor,
                         const py::object& cPoint) {
            const Real nr = Null<Real>();
            std::pair<Real, Real> cp(nr, nr);
            if (!cPoint.is_none())
                cp = cPoint.cast<std::pair<Real, Real>>();
            return ext::make_shared<FdmCEV1dMesher>(
                size, f0, alpha, beta, maturity, eps, scaleFactor, cp);
        }),
            py::arg("size"),
            py::arg("f0"), py::arg("alpha"), py::arg("beta"),
            py::arg("maturity"),
            py::arg("eps") = 0.0001,
            py::arg("scaleFactor") = 1.5,
            py::arg("cPoint") = py::none(),
            "Constructs a CEV mesher.");
}
