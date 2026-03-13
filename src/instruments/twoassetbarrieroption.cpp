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
#include <ql/instruments/twoassetbarrieroption.hpp>
#include <ql/exercise.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::twoassetbarrieroption(py::module_& m) {
    py::class_<TwoAssetBarrierOption, Option,
               ext::shared_ptr<TwoAssetBarrierOption>>(
        m, "TwoAssetBarrierOption",
        "Barrier option on two assets.")
        .def(py::init<Barrier::Type, Real,
                      const ext::shared_ptr<StrikedTypePayoff>&,
                      const ext::shared_ptr<Exercise>&>(),
            py::arg("barrierType"),
            py::arg("barrier"),
            py::arg("payoff"),
            py::arg("exercise"),
            "Constructs a two-asset barrier option.")
        .def("isExpired", &TwoAssetBarrierOption::isExpired,
            "Returns whether the option is expired.");
}
