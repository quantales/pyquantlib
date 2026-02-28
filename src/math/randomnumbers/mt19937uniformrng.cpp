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
#include <ql/math/randomnumbers/mt19937uniformrng.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::mt19937uniformrng(py::module_& m) {
    py::class_<MersenneTwisterUniformRng>(m, "MersenneTwisterUniformRng",
        "Mersenne Twister uniform random number generator (period 2^19937-1).")
        .def(py::init<unsigned long>(),
            py::arg("seed") = 0,
            "Constructs with seed (0 for clock-based random seed).")
        .def(py::init<const std::vector<unsigned long>&>(),
            py::arg("seeds"),
            "Constructs with a vector of seeds.")
        .def("next", &MersenneTwisterUniformRng::next,
            "Returns a sample with value in (0, 1) and weight 1.")
        .def("nextReal", &MersenneTwisterUniformRng::nextReal,
            "Returns a random number in (0, 1).")
        .def("nextInt32", &MersenneTwisterUniformRng::nextInt32,
            "Returns a random 32-bit unsigned integer.");
}
