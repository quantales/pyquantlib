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
#include "pyquantlib/trampolines.h"
#include <ql/exercise.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_core::exercise(py::module_& m) {
    py::class_<Exercise, PyExercise, ext::shared_ptr<Exercise>>(m, "Exercise",
        "Abstract base class for option exercise styles.")
        .def("dates", &Exercise::dates,
            "Returns the list of exercise dates.")
        .def("lastDate", &Exercise::lastDate,
            "Returns the latest exercise date.");

    py::class_<EuropeanExercise, Exercise, ext::shared_ptr<EuropeanExercise>>(
        m, "EuropeanExercise", "European-style exercise (single date).")
        .def(py::init<const Date&>(),
            py::arg("date"),
            "Constructs with the exercise date.");

    py::class_<AmericanExercise, Exercise, ext::shared_ptr<AmericanExercise>>(
        m, "AmericanExercise", "American-style exercise (date range).")
        .def(py::init<const Date&, const Date&>(),
            py::arg("earliestDate"), py::arg("latestDate"),
            "Constructs with earliest and latest exercise dates.");

    py::class_<BermudanExercise, Exercise, ext::shared_ptr<BermudanExercise>>(
        m, "BermudanExercise", "Bermudan-style exercise (discrete dates).")
        .def(py::init<const std::vector<Date>&>(),
            py::arg("dates"),
            "Constructs with a list of exercise dates.");
}
