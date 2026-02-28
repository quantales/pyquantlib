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
#include <ql/math/randomnumbers/burley2020sobolrsg.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::burley2020sobolrsg(py::module_& m) {
    py::class_<Burley2020SobolRsg>(m, "Burley2020SobolRsg",
        "Scrambled Sobol sequence (Burley 2020 hash-based Owen scrambling).")
        .def(py::init<Size, unsigned long, SobolRsg::DirectionIntegers,
                      unsigned long>(),
            py::arg("dimensionality"),
            py::arg("seed") = 42,
            py::arg("directionIntegers") = SobolRsg::Jaeckel,
            py::arg("scrambleSeed") = 43,
            "Constructs scrambled Sobol sequence generator.")
        .def("nextSequence", &Burley2020SobolRsg::nextSequence,
            py::return_value_policy::copy,
            "Returns next sample sequence.")
        .def("lastSequence", &Burley2020SobolRsg::lastSequence,
            py::return_value_policy::copy,
            "Returns the last generated sequence.")
        .def("dimension", &Burley2020SobolRsg::dimension,
            "Returns the dimensionality.")
        .def("skipTo", [](Burley2020SobolRsg& self, unsigned long n) {
                self.skipTo(static_cast<std::uint32_t>(n));
            },
            py::arg("n"),
            "Skips to the n-th sample in the sequence.");
}
