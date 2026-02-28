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
#include <ql/experimental/variancegamma/variancegammamodel.hpp>
#include <ql/experimental/variancegamma/variancegammaprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_experimental::variancegammamodel(py::module_& m) {
    py::class_<VarianceGammaModel, CalibratedModel,
               ext::shared_ptr<VarianceGammaModel>>(
        m, "VarianceGammaModel",
        "Variance Gamma calibrated model.")
        .def(py::init<const ext::shared_ptr<VarianceGammaProcess>&>(),
             py::arg("process"))
        .def("sigma", &VarianceGammaModel::sigma,
             "Returns sigma.")
        .def("nu", &VarianceGammaModel::nu,
             "Returns nu.")
        .def("theta", &VarianceGammaModel::theta,
             "Returns theta.")
        .def("process", &VarianceGammaModel::process,
             "Returns the underlying process.");
}
