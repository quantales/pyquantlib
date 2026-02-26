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
#include <ql/instruments/forwardvanillaoption.hpp>
#include <ql/instruments/payoffs.hpp>
#include <ql/exercise.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::forwardvanillaoption(py::module_& m) {
    py::class_<ForwardVanillaOption, OneAssetOption,
               ext::shared_ptr<ForwardVanillaOption>>(
        m, "ForwardVanillaOption",
        "Forward-start vanilla option.")
        .def(py::init<Real, const Date&,
                      const ext::shared_ptr<StrikedTypePayoff>&,
                      const ext::shared_ptr<Exercise>&>(),
             py::arg("moneyness"),
             py::arg("resetDate"),
             py::arg("payoff"),
             py::arg("exercise"));
}
