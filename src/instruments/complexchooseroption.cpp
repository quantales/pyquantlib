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
#include <ql/instruments/complexchooseroption.hpp>
#include <ql/exercise.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::complexchooseroption(py::module_& m) {
    py::class_<ComplexChooserOption, OneAssetOption,
               ext::shared_ptr<ComplexChooserOption>>(
        m, "ComplexChooserOption",
        "Complex chooser option (different strikes and exercises for call/put).")
        .def(py::init<Date, Real, Real,
                      const ext::shared_ptr<Exercise>&,
                      ext::shared_ptr<Exercise>>(),
             py::arg("choosingDate"),
             py::arg("strikeCall"),
             py::arg("strikePut"),
             py::arg("exerciseCall"),
             py::arg("exercisePut"));
}
