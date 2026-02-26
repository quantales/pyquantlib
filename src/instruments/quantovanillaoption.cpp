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
#include <ql/instruments/quantovanillaoption.hpp>
#include <ql/instruments/payoffs.hpp>
#include <ql/exercise.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::quantovanillaoption(py::module_& m) {
    py::class_<QuantoVanillaOption, OneAssetOption,
               ext::shared_ptr<QuantoVanillaOption>>(
        m, "QuantoVanillaOption",
        "Quanto vanilla option (currency-adjusted).")
        .def(py::init<const ext::shared_ptr<StrikedTypePayoff>&,
                      const ext::shared_ptr<Exercise>&>(),
             py::arg("payoff"),
             py::arg("exercise"))
        .def("qvega", &QuantoVanillaOption::qvega,
            "Returns quanto vega.")
        .def("qrho", &QuantoVanillaOption::qrho,
            "Returns quanto rho.")
        .def("qlambda", &QuantoVanillaOption::qlambda,
            "Returns quanto lambda (correlation sensitivity).");
}
