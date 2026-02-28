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
#include <ql/math/randomnumbers/sobolrsg.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::sobolrsg(py::module_& m) {
    auto cls = py::class_<SobolRsg>(m, "SobolRsg",
        "Sobol low-discrepancy sequence generator.");

    py::enum_<SobolRsg::DirectionIntegers>(cls, "DirectionIntegers",
        "Direction integer sets for Sobol sequences.")
        .value("Unit", SobolRsg::Unit)
        .value("Jaeckel", SobolRsg::Jaeckel)
        .value("SobolLevitan", SobolRsg::SobolLevitan)
        .value("SobolLevitanLemieux", SobolRsg::SobolLevitanLemieux)
        .value("JoeKuoD5", SobolRsg::JoeKuoD5)
        .value("JoeKuoD6", SobolRsg::JoeKuoD6)
        .value("JoeKuoD7", SobolRsg::JoeKuoD7)
        .value("Kuo", SobolRsg::Kuo)
        .value("Kuo2", SobolRsg::Kuo2)
        .value("Kuo3", SobolRsg::Kuo3)
        .export_values();

    cls
        .def(py::init<Size, unsigned long, SobolRsg::DirectionIntegers, bool>(),
            py::arg("dimensionality"),
            py::arg("seed") = 0,
            py::arg("directionIntegers") = SobolRsg::Jaeckel,
            py::arg("useGrayCode") = true,
            "Constructs Sobol sequence generator.")
        .def("nextSequence", &SobolRsg::nextSequence,
            py::return_value_policy::copy,
            "Returns next sample sequence.")
        .def("lastSequence", &SobolRsg::lastSequence,
            py::return_value_policy::copy,
            "Returns the last generated sequence.")
        .def("dimension", &SobolRsg::dimension,
            "Returns the dimensionality.")
        .def("skipTo", [](SobolRsg& self, unsigned long n) {
                self.skipTo(static_cast<std::uint32_t>(n));
            },
            py::arg("n"),
            "Skips to the n-th sample in the sequence.");
}
