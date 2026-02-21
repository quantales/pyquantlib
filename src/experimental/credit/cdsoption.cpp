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
#include <ql/experimental/credit/cdsoption.hpp>
#include <ql/instruments/creditdefaultswap.hpp>
#include <ql/exercise.hpp>
#include <ql/termstructures/defaulttermstructure.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_experimental::cdsoption(py::module_& m) {
    py::class_<CdsOption, Option, ext::shared_ptr<CdsOption>>(
        m, "CdsOption",
        "Option on a credit default swap.")
        .def(py::init<const ext::shared_ptr<CreditDefaultSwap>&,
                      const ext::shared_ptr<Exercise>&, bool>(),
            py::arg("swap"),
            py::arg("exercise"),
            py::arg("knocksOut") = true,
            "Constructs a CDS option.")
        .def("underlyingSwap", &CdsOption::underlyingSwap,
            "Returns the underlying CDS.")
        .def("atmRate", &CdsOption::atmRate,
            "Returns the at-the-money rate.")
        .def("riskyAnnuity", &CdsOption::riskyAnnuity,
            "Returns the risky annuity.")
        // Handle-based impliedVolatility
        .def("impliedVolatility", &CdsOption::impliedVolatility,
            py::arg("price"),
            py::arg("termStructure"),
            py::arg("defaultProbTS"),
            py::arg("recoveryRate"),
            py::arg("accuracy") = 1.0e-4,
            py::arg("maxEvaluations") = 100,
            py::arg("minVol") = 1.0e-7,
            py::arg("maxVol") = 4.0,
            "Returns the implied volatility.")
        // Hidden handle impliedVolatility
        .def("impliedVolatility",
            [](const CdsOption& self,
               Real price,
               const ext::shared_ptr<YieldTermStructure>& termStructure,
               const ext::shared_ptr<DefaultProbabilityTermStructure>& defaultProbTS,
               Real recoveryRate,
               Real accuracy,
               Size maxEvaluations,
               Volatility minVol,
               Volatility maxVol) {
                return self.impliedVolatility(
                    price,
                    Handle<YieldTermStructure>(termStructure),
                    Handle<DefaultProbabilityTermStructure>(defaultProbTS),
                    recoveryRate, accuracy, maxEvaluations, minVol, maxVol);
            },
            py::arg("price"),
            py::arg("termStructure"),
            py::arg("defaultProbTS"),
            py::arg("recoveryRate"),
            py::arg("accuracy") = 1.0e-4,
            py::arg("maxEvaluations") = 100,
            py::arg("minVol") = 1.0e-7,
            py::arg("maxVol") = 4.0,
            "Returns the implied volatility (handles created internally).");
}
