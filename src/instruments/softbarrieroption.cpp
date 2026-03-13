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
#include <ql/instruments/softbarrieroption.hpp>
#include <ql/exercise.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::softbarrieroption(py::module_& m) {
    py::class_<SoftBarrierOption, OneAssetOption,
               ext::shared_ptr<SoftBarrierOption>>(
        m, "SoftBarrierOption",
        "Soft barrier option (proportional knock-in/out over barrier range).")
        .def(py::init<Barrier::Type, Real, Real,
                      const ext::shared_ptr<StrikedTypePayoff>&,
                      const ext::shared_ptr<Exercise>&>(),
            py::arg("barrierType"),
            py::arg("barrierLo"),
            py::arg("barrierHi"),
            py::arg("payoff"),
            py::arg("exercise"),
            "Constructs a soft barrier option.")
        .def("impliedVolatility",
            &SoftBarrierOption::impliedVolatility,
            py::arg("price"),
            py::arg("process"),
            py::arg("accuracy") = 1.0e-4,
            py::arg("maxEvaluations") = 100,
            py::arg("minVol") = 1.0e-6,
            py::arg("maxVol") = 4.0,
            "Returns implied volatility.");
}
