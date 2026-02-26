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
#include <ql/instruments/cliquetoption.hpp>
#include <ql/instruments/payoffs.hpp>
#include <ql/exercise.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::cliquetoption(py::module_& m) {
    py::class_<CliquetOption, OneAssetOption,
               ext::shared_ptr<CliquetOption>>(
        m, "CliquetOption",
        "Cliquet (ratchet) option with periodic resets.")
        .def(py::init<const ext::shared_ptr<PercentageStrikePayoff>&,
                      const ext::shared_ptr<EuropeanExercise>&,
                      std::vector<Date>>(),
             py::arg("payoff"),
             py::arg("maturity"),
             py::arg("resetDates"));
}
