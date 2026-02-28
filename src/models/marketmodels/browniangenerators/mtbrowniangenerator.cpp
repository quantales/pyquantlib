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
#include <ql/models/marketmodels/browniangenerators/mtbrowniangenerator.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::mtbrowniangenerator(py::module_& m) {
    py::class_<MTBrownianGenerator, BrownianGenerator,
               ext::shared_ptr<MTBrownianGenerator>>(m, "MTBrownianGenerator",
        "Mersenne-Twister Brownian generator.")
        .def(py::init<Size, Size, unsigned long>(),
            py::arg("factors"), py::arg("steps"), py::arg("seed") = 0,
            "Constructs from dimensions and optional seed.");

    py::class_<MTBrownianGeneratorFactory, BrownianGeneratorFactory,
               ext::shared_ptr<MTBrownianGeneratorFactory>>(
        m, "MTBrownianGeneratorFactory",
        "Factory for Mersenne-Twister Brownian generators.")
        .def(py::init<unsigned long>(),
            py::arg("seed") = 0,
            "Constructs with optional seed.");
}
