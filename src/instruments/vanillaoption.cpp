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
#include <ql/instruments/vanillaoption.hpp>
#include <ql/instruments/oneassetoption.hpp>
#include <ql/instruments/payoffs.hpp>
#include <ql/exercise.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::vanillaoption(py::module_& m) {
    py::class_<VanillaOption, OneAssetOption, ext::shared_ptr<VanillaOption>>(
        m, "VanillaOption",
        "Plain vanilla option on a single asset.")
        .def(py::init<const ext::shared_ptr<StrikedTypePayoff>&,
                      const ext::shared_ptr<Exercise>&>(),
             py::arg("payoff"), py::arg("exercise"));
}
