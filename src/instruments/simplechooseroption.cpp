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
#include <ql/instruments/simplechooseroption.hpp>
#include <ql/exercise.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::simplechooseroption(py::module_& m) {
    py::class_<SimpleChooserOption, OneAssetOption,
               ext::shared_ptr<SimpleChooserOption>>(
        m, "SimpleChooserOption",
        "Simple chooser option (choose call or put at choosing date).")
        .def(py::init<Date, Real, const ext::shared_ptr<Exercise>&>(),
             py::arg("choosingDate"),
             py::arg("strike"),
             py::arg("exercise"));
}
