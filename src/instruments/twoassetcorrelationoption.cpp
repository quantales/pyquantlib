/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/instruments/twoassetcorrelationoption.hpp>
#include <ql/exercise.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::twoassetcorrelationoption(py::module_& m) {
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
