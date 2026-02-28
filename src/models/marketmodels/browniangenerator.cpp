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
#include <ql/models/marketmodels/browniangenerator.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::browniangenerator(py::module_& m) {
    py::class_<BrownianGenerator, ext::shared_ptr<BrownianGenerator>>(
        m, "BrownianGenerator",
        "Abstract base class for Brownian generators.")
        .def("nextStep", [](BrownianGenerator& gen) {
            std::vector<Real> output(gen.numberOfFactors());
            Real weight = gen.nextStep(output);
            return py::make_tuple(weight, output);
        }, "Returns (weight, variates) for the next time step.")
        .def("nextPath", &BrownianGenerator::nextPath,
            "Starts a new path and returns its weight.")
        .def("numberOfFactors", &BrownianGenerator::numberOfFactors,
            "Number of factors.")
        .def("numberOfSteps", &BrownianGenerator::numberOfSteps,
            "Number of time steps.");

    py::class_<BrownianGeneratorFactory,
               ext::shared_ptr<BrownianGeneratorFactory>>(
        m, "BrownianGeneratorFactory",
        "Abstract factory for Brownian generators.")
        .def("create", &BrownianGeneratorFactory::create,
            py::arg("factors"), py::arg("steps"),
            "Creates a Brownian generator for the given dimensions.");
}
