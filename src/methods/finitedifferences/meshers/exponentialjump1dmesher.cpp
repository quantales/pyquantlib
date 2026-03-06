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
#include <ql/methods/finitedifferences/meshers/exponentialjump1dmesher.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::exponentialjump1dmesher(py::module_& m) {
    py::class_<ExponentialJump1dMesher, Fdm1dMesher,
               ext::shared_ptr<ExponentialJump1dMesher>>(
        m, "ExponentialJump1dMesher",
        "1D mesher for exponential jump-diffusion processes.")
        .def(py::init<Size, Real, Real, Real, Real>(),
            py::arg("steps"), py::arg("beta"),
            py::arg("jumpIntensity"), py::arg("eta"),
            py::arg("eps") = 1e-3,
            "Constructs with step count and jump parameters.")
        .def("jumpSizeDensity",
            py::overload_cast<Real>(&ExponentialJump1dMesher::jumpSizeDensity, py::const_),
            py::arg("x"),
            "Asymptotic jump size density (t -> infinity).")
        .def("jumpSizeDensity",
            py::overload_cast<Real, Time>(&ExponentialJump1dMesher::jumpSizeDensity, py::const_),
            py::arg("x"), py::arg("t"),
            "Time-dependent jump size density.")
        .def("jumpSizeDistribution",
            py::overload_cast<Real>(&ExponentialJump1dMesher::jumpSizeDistribution, py::const_),
            py::arg("x"),
            "Asymptotic jump size distribution.")
        .def("jumpSizeDistribution",
            py::overload_cast<Real, Time>(&ExponentialJump1dMesher::jumpSizeDistribution, py::const_),
            py::arg("x"), py::arg("t"),
            "Time-dependent jump size distribution.");
}
