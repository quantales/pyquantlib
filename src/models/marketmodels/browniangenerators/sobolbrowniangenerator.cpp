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
#include <ql/models/marketmodels/browniangenerators/sobolbrowniangenerator.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::sobolbrowniangenerator(py::module_& m) {
    py::enum_<SobolBrownianGeneratorBase::Ordering>(m, "Ordering",
        "Ordering schemes for Sobol Brownian generators.")
        .value("Factors", SobolBrownianGeneratorBase::Factors,
            "Best-quality variates for the first factor.")
        .value("Steps", SobolBrownianGeneratorBase::Steps,
            "Best-quality variates for the largest steps.")
        .value("Diagonal", SobolBrownianGeneratorBase::Diagonal,
            "Diagonal schema balancing factors and steps.")
        .export_values();

    py::class_<SobolBrownianGenerator, BrownianGenerator,
               ext::shared_ptr<SobolBrownianGenerator>>(
        m, "SobolBrownianGenerator",
        "Sobol Brownian generator with Brownian bridging.")
        .def(py::init<Size, Size, SobolBrownianGeneratorBase::Ordering,
                       unsigned long, SobolRsg::DirectionIntegers>(),
            py::arg("factors"), py::arg("steps"),
            py::arg("ordering"),
            py::arg("seed") = 0,
            py::arg("directionIntegers") = SobolRsg::Jaeckel,
            "Constructs a Sobol Brownian generator.");

    py::class_<SobolBrownianGeneratorFactory, BrownianGeneratorFactory,
               ext::shared_ptr<SobolBrownianGeneratorFactory>>(
        m, "SobolBrownianGeneratorFactory",
        "Factory for Sobol Brownian generators.")
        .def(py::init<SobolBrownianGeneratorBase::Ordering,
                       unsigned long, SobolRsg::DirectionIntegers>(),
            py::arg("ordering"),
            py::arg("seed") = 0,
            py::arg("directionIntegers") = SobolRsg::Jaeckel,
            "Constructs a Sobol Brownian generator factory.");

    py::class_<Burley2020SobolBrownianGenerator, BrownianGenerator,
               ext::shared_ptr<Burley2020SobolBrownianGenerator>>(
        m, "Burley2020SobolBrownianGenerator",
        "Scrambled Sobol Brownian generator with Brownian bridging.")
        .def(py::init<Size, Size, SobolBrownianGeneratorBase::Ordering,
                       unsigned long, SobolRsg::DirectionIntegers,
                       unsigned long>(),
            py::arg("factors"), py::arg("steps"),
            py::arg("ordering"),
            py::arg("seed") = 42,
            py::arg("directionIntegers") = SobolRsg::Jaeckel,
            py::arg("scrambleSeed") = 43,
            "Constructs a scrambled Sobol Brownian generator.");

    py::class_<Burley2020SobolBrownianGeneratorFactory,
               BrownianGeneratorFactory,
               ext::shared_ptr<Burley2020SobolBrownianGeneratorFactory>>(
        m, "Burley2020SobolBrownianGeneratorFactory",
        "Factory for scrambled Sobol Brownian generators.")
        .def(py::init<SobolBrownianGeneratorBase::Ordering,
                       unsigned long, SobolRsg::DirectionIntegers,
                       unsigned long>(),
            py::arg("ordering"),
            py::arg("seed") = 42,
            py::arg("directionIntegers") = SobolRsg::Jaeckel,
            py::arg("scrambleSeed") = 43,
            "Constructs a scrambled Sobol Brownian generator factory.");
}
