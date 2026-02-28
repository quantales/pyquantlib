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
#include <ql/experimental/variancegamma/fftvariancegammaengine.hpp>
#include <ql/experimental/variancegamma/variancegammaprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_experimental::fftvariancegammaengine(py::module_& m) {
    py::class_<FFTVarianceGammaEngine, PricingEngine,
               ext::shared_ptr<FFTVarianceGammaEngine>>(
        m, "FFTVarianceGammaEngine",
        "FFT Variance Gamma option engine.")
        .def(py::init<const ext::shared_ptr<VarianceGammaProcess>&, Real>(),
             py::arg("process"),
             py::arg("logStrikeSpacing") = 0.001);
}
