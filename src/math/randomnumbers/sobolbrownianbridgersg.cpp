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
#include <ql/math/randomnumbers/sobolbrownianbridgersg.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::sobolbrownianbridgersg(py::module_& m) {
    py::class_<SobolBrownianBridgeRsg>(m, "SobolBrownianBridgeRsg",
        "Sobol quasi-random sequence generator with Brownian bridge ordering.")
        .def(py::init<Size, Size, SobolBrownianGenerator::Ordering,
                      unsigned long, SobolRsg::DirectionIntegers>(),
            py::arg("factors"),
            py::arg("steps"),
            py::arg("ordering") = SobolBrownianGenerator::Diagonal,
            py::arg("seed") = 0,
            py::arg("directionIntegers") = SobolRsg::JoeKuoD7,
            "Constructs Sobol Brownian bridge sequence generator.")
        .def("nextSequence", &SobolBrownianBridgeRsg::nextSequence,
            py::return_value_policy::copy,
            "Returns next sample sequence.")
        .def("lastSequence", &SobolBrownianBridgeRsg::lastSequence,
            py::return_value_policy::copy,
            "Returns the last generated sequence.")
        .def("dimension", &SobolBrownianBridgeRsg::dimension,
            "Returns the dimensionality (factors x steps).");

    py::class_<Burley2020SobolBrownianBridgeRsg>(m,
        "Burley2020SobolBrownianBridgeRsg",
        "Scrambled Sobol quasi-random sequence generator with Brownian bridge "
        "ordering (Burley 2020 hash-based Owen scrambling).")
        .def(py::init<Size, Size, SobolBrownianGenerator::Ordering,
                      unsigned long, SobolRsg::DirectionIntegers,
                      unsigned long>(),
            py::arg("factors"),
            py::arg("steps"),
            py::arg("ordering") = SobolBrownianGenerator::Diagonal,
            py::arg("seed") = 42,
            py::arg("directionIntegers") = SobolRsg::JoeKuoD7,
            py::arg("scrambleSeed") = 43,
            "Constructs scrambled Sobol Brownian bridge sequence generator.")
        .def("nextSequence",
            &Burley2020SobolBrownianBridgeRsg::nextSequence,
            py::return_value_policy::copy,
            "Returns next sample sequence.")
        .def("lastSequence",
            &Burley2020SobolBrownianBridgeRsg::lastSequence,
            py::return_value_policy::copy,
            "Returns the last generated sequence.")
        .def("dimension", &Burley2020SobolBrownianBridgeRsg::dimension,
            "Returns the dimensionality (factors x steps).");
}
