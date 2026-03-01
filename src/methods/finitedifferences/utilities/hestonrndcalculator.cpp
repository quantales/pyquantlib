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
#include <ql/methods/finitedifferences/utilities/hestonrndcalculator.hpp>
#include <ql/processes/hestonprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::hestonrndcalculator(py::module_& m) {
    py::class_<HestonRNDCalculator,
               ext::shared_ptr<HestonRNDCalculator>,
               RiskNeutralDensityCalculator>(
        m, "HestonRNDCalculator",
        "Heston model risk-neutral density calculator.")
        .def(py::init<ext::shared_ptr<HestonProcess>, Real, Size>(),
            py::arg("hestonProcess"),
            py::arg("integrationEps") = 1e-6,
            py::arg("maxIntegrationIterations") = Size(10000),
            "Constructs with Heston process and integration parameters.");
}
