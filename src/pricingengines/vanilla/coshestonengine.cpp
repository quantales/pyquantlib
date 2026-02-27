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
#include <ql/pricingengines/vanilla/coshestonengine.hpp>
#include <ql/models/equity/hestonmodel.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/complex.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::coshestonengine(py::module_& m) {
    py::class_<COSHestonEngine,
               ext::shared_ptr<COSHestonEngine>,
               PricingEngine>(
        m, "COSHestonEngine",
        "Heston engine using Fourier-cosine series expansion.")
        .def(py::init<const ext::shared_ptr<HestonModel>&, Real, Size>(),
            py::arg("model"),
            py::arg("L") = 16,
            py::arg("N") = 200,
            "Constructs COS Heston engine.")
        .def("chF", &COSHestonEngine::chF,
            py::arg("u"), py::arg("t"),
            "Returns the normalized characteristic function.")
        .def("c1", &COSHestonEngine::c1, py::arg("t"))
        .def("c2", &COSHestonEngine::c2, py::arg("t"))
        .def("c3", &COSHestonEngine::c3, py::arg("t"))
        .def("c4", &COSHestonEngine::c4, py::arg("t"))
        .def("mu", &COSHestonEngine::mu, py::arg("t"),
            "Returns the mean.")
        .def("var", &COSHestonEngine::var, py::arg("t"),
            "Returns the variance.")
        .def("skew", &COSHestonEngine::skew, py::arg("t"),
            "Returns the skewness.")
        .def("kurtosis", &COSHestonEngine::kurtosis, py::arg("t"),
            "Returns the kurtosis.");
}
