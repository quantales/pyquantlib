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
#include <ql/math/randomnumbers/randomsequencegenerator.hpp>
#include <ql/math/randomnumbers/mt19937uniformrng.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::randomsequencegenerator(py::module_& m) {
    using UniformRsg = RandomSequenceGenerator<MersenneTwisterUniformRng>;

    py::class_<UniformRsg>(m, "UniformRandomSequenceGenerator",
        "Uniform random sequence generator (uses Mersenne Twister).")
        .def(py::init<Size, const MersenneTwisterUniformRng&>(),
            py::arg("dimensionality"),
            py::arg("rng"),
            "Constructs from dimensionality and a uniform RNG.")
        .def(py::init<Size, BigNatural>(),
            py::arg("dimensionality"),
            py::arg("seed") = 0,
            "Constructs from dimensionality and seed.")
        .def("nextSequence", &UniformRsg::nextSequence,
            py::return_value_policy::copy,
            "Returns next sample sequence.")
        .def("lastSequence", &UniformRsg::lastSequence,
            py::return_value_policy::copy,
            "Returns the last generated sequence.")
        .def("nextInt32Sequence", &UniformRsg::nextInt32Sequence,
            "Returns next sequence of 32-bit unsigned integers.")
        .def("dimension", &UniformRsg::dimension,
            "Returns the dimensionality.");
}
