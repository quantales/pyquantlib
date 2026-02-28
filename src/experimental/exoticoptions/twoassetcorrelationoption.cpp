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
#include <ql/experimental/exoticoptions/twoassetcorrelationoption.hpp>
#include <ql/exercise.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_experimental::twoassetcorrelationoption(py::module_& m) {
    py::class_<TwoAssetCorrelationOption, MultiAssetOption,
               ext::shared_ptr<TwoAssetCorrelationOption>>(
        m, "TwoAssetCorrelationOption",
        "Two-asset correlation option.")
        .def(py::init<Option::Type, Real, Real,
                      const ext::shared_ptr<Exercise>&>(),
             py::arg("type"),
             py::arg("strike1"),
             py::arg("strike2"),
             py::arg("exercise"));
}
