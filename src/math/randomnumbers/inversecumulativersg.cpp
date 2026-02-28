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
#include <ql/math/randomnumbers/inversecumulativersg.hpp>
#include <ql/math/randomnumbers/randomsequencegenerator.hpp>
#include <ql/math/randomnumbers/mt19937uniformrng.hpp>
#include <ql/math/randomnumbers/sobolrsg.hpp>
#include <ql/math/distributions/normaldistribution.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::inversecumulativersg(py::module_& m) {
    // Gaussian pseudo-random sequence generator
    using UniformRsg = RandomSequenceGenerator<MersenneTwisterUniformRng>;
    using GaussianRsg = InverseCumulativeRsg<UniformRsg, InverseCumulativeNormal>;

    py::class_<GaussianRsg>(m, "GaussianRandomSequenceGenerator",
        "Gaussian random sequence generator via inverse cumulative normal "
        "(uses Mersenne Twister).")
        .def(py::init<const UniformRsg&>(),
            py::arg("uniformSequenceGenerator"),
            "Constructs from a uniform random sequence generator.")
        .def(py::init([](Size dimensionality, unsigned long seed) {
                return GaussianRsg(UniformRsg(dimensionality, seed));
            }),
            py::arg("dimensionality"),
            py::arg("seed") = 0,
            "Constructs from dimensionality and seed.")
        .def("nextSequence", &GaussianRsg::nextSequence,
            py::return_value_policy::copy,
            "Returns next Gaussian sample sequence.")
        .def("lastSequence", &GaussianRsg::lastSequence,
            py::return_value_policy::copy,
            "Returns the last generated sequence.")
        .def("dimension", &GaussianRsg::dimension,
            "Returns the dimensionality.");

    // Gaussian low-discrepancy sequence generator (Sobol-based)
    using GaussianLdsg = InverseCumulativeRsg<SobolRsg, InverseCumulativeNormal>;

    py::class_<GaussianLdsg>(m, "GaussianLowDiscrepancySequenceGenerator",
        "Gaussian low-discrepancy sequence generator via inverse cumulative "
        "normal (uses Sobol).")
        .def(py::init<const SobolRsg&>(),
            py::arg("uniformSequenceGenerator"),
            "Constructs from a Sobol sequence generator.")
        .def(py::init([](Size dimensionality, unsigned long seed,
                         SobolRsg::DirectionIntegers directionIntegers) {
                return GaussianLdsg(
                    SobolRsg(dimensionality, seed, directionIntegers));
            }),
            py::arg("dimensionality"),
            py::arg("seed") = 0,
            py::arg("directionIntegers") = SobolRsg::Jaeckel,
            "Constructs from dimensionality, seed, and direction integers.")
        .def("nextSequence", &GaussianLdsg::nextSequence,
            py::return_value_policy::copy,
            "Returns next Gaussian sample sequence.")
        .def("lastSequence", &GaussianLdsg::lastSequence,
            py::return_value_policy::copy,
            "Returns the last generated sequence.")
        .def("dimension", &GaussianLdsg::dimension,
            "Returns the dimensionality.");
}
