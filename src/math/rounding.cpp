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
#include <ql/math/rounding.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::rounding(py::module_& m) {
    py::class_<Rounding> pyRounding(m, "Rounding",
        "Basic rounding convention.");

    py::enum_<Rounding::Type>(pyRounding, "Type",
        "Rounding type enumeration.")
        .value("None_", Rounding::Type::None, "No rounding.")
        .value("Up", Rounding::Type::Up, "Round up.")
        .value("Down", Rounding::Type::Down, "Round down.")
        .value("Closest", Rounding::Type::Closest, "Round to the closest.")
        .value("Floor", Rounding::Type::Floor,
            "Round to the largest integer not greater than x.")
        .value("Ceiling", Rounding::Type::Ceiling,
            "Round to the smallest integer not less than x.");

    pyRounding
        .def(py::init<Integer, Rounding::Type, Integer>(),
            py::arg("precision"),
            py::arg("type") = Rounding::Type::Closest,
            py::arg("digit") = 5,
            "Creates a rounding convention.")
        .def_property_readonly("precision", &Rounding::precision,
            "Returns the precision.")
        .def_property_readonly("type", &Rounding::type,
            "Returns the rounding type.")
        .def_property_readonly("roundingDigit", &Rounding::roundingDigit,
            "Returns the rounding digit.")
        .def("__call__", [](const Rounding& self, Decimal value) {
                return self(value);
            },
            py::arg("value"),
            "Rounds the given value.");

    // Concrete rounding implementations
    py::class_<UpRounding, Rounding>(m, "UpRounding",
        "Up-rounding.")
        .def(py::init<Integer, Integer>(),
            py::arg("precision"), py::arg("digit") = 5);

    py::class_<DownRounding, Rounding>(m, "DownRounding",
        "Down-rounding.")
        .def(py::init<Integer, Integer>(),
            py::arg("precision"), py::arg("digit") = 5);

    py::class_<ClosestRounding, Rounding>(m, "ClosestRounding",
        "Closest-rounding.")
        .def(py::init<Integer, Integer>(),
            py::arg("precision"), py::arg("digit") = 5);

    py::class_<CeilingTruncation, Rounding>(m, "CeilingTruncation",
        "Ceiling truncation.")
        .def(py::init<Integer, Integer>(),
            py::arg("precision"), py::arg("digit") = 5);

    py::class_<FloorTruncation, Rounding>(m, "FloorTruncation",
        "Floor truncation.")
        .def(py::init<Integer, Integer>(),
            py::arg("precision"), py::arg("digit") = 5);
}
