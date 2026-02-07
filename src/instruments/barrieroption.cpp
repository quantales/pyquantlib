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
#include <ql/instruments/barrieroption.hpp>
#include <ql/instruments/barriertype.hpp>
#include <ql/exercise.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::barrieroption(py::module_& m) {
    py::class_<BarrierOption, OneAssetOption, ext::shared_ptr<BarrierOption>>(
        m, "BarrierOption",
        "Barrier option on a single asset.")
        .def(py::init<Barrier::Type, Real, Real,
                       const ext::shared_ptr<StrikedTypePayoff>&,
                       const ext::shared_ptr<Exercise>&>(),
            py::arg("barrierType"),
            py::arg("barrier"),
            py::arg("rebate"),
            py::arg("payoff"),
            py::arg("exercise"),
            "Constructs BarrierOption.")
        .def("impliedVolatility",
            py::overload_cast<Real,
                              const ext::shared_ptr<GeneralizedBlackScholesProcess>&,
                              Real, Size, Volatility, Volatility>(
                &BarrierOption::impliedVolatility, py::const_),
            py::arg("price"),
            py::arg("process"),
            py::arg("accuracy") = 1.0e-4,
            py::arg("maxEvaluations") = 100,
            py::arg("minVol") = 1.0e-7,
            py::arg("maxVol") = 4.0,
            "Returns implied volatility.");
}
