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
#include <ql/math/randomnumbers/boxmullergaussianrng.hpp>
#include <ql/math/randomnumbers/mt19937uniformrng.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::boxmullergaussianrng(py::module_& m) {
    using BoxMullerMT = BoxMullerGaussianRng<MersenneTwisterUniformRng>;

    py::class_<BoxMullerMT>(m, "BoxMullerGaussianRng",
        "Box-Muller Gaussian random number generator (uses Mersenne Twister).")
        .def(py::init<const MersenneTwisterUniformRng&>(),
            py::arg("uniformGenerator"),
            "Constructs from a uniform random number generator.")
        .def(py::init([](unsigned long seed) {
                return BoxMullerMT(MersenneTwisterUniformRng(seed));
            }),
            py::arg("seed") = 0,
            "Constructs with seed (0 for clock-based random seed).")
        .def("next", &BoxMullerMT::next,
            "Returns a sample with Gaussian deviate and weight.");
}
