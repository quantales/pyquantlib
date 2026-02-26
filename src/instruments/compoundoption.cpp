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
#include <ql/instruments/compoundoption.hpp>
#include <ql/instruments/payoffs.hpp>
#include <ql/exercise.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::compoundoption(py::module_& m) {
    py::class_<CompoundOption, OneAssetOption,
               ext::shared_ptr<CompoundOption>>(
        m, "CompoundOption",
        "Option on an option (compound option).")
        .def(py::init<const ext::shared_ptr<StrikedTypePayoff>&,
                      const ext::shared_ptr<Exercise>&,
                      ext::shared_ptr<StrikedTypePayoff>,
                      ext::shared_ptr<Exercise>>(),
             py::arg("motherPayoff"),
             py::arg("motherExercise"),
             py::arg("daughterPayoff"),
             py::arg("daughterExercise"));
}
