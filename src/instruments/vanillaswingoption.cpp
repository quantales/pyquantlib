/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/instruments/vanillaswingoption.hpp>
#include <ql/exercise.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::vanillaswingoption(py::module_& m) {
    py::class_<SwingExercise, BermudanExercise, ext::shared_ptr<SwingExercise>>(
        m, "SwingExercise",
        "Exercise for swing options: a fixed set of exercisable date-times.")
        .def(py::init<const std::vector<Date>&, const std::vector<Size>&>(),
            py::arg("dates"), py::arg("seconds") = std::vector<Size>(),
            "Constructs from exercise dates, with optional intraday seconds offsets.")
        .def(py::init<const Date&, const Date&, Size>(),
            py::arg("from"), py::arg("to"), py::arg("stepSizeSecs"),
            "Constructs from a date range stepped at a fixed number of seconds.")
        .def("seconds", &SwingExercise::seconds,
            "Returns the intraday seconds offset for each exercise date.");

    py::class_<VanillaForwardPayoff, StrikedTypePayoff,
               ext::shared_ptr<VanillaForwardPayoff>>(
        m, "VanillaForwardPayoff", "Forward-type vanilla payoff.")
        .def(py::init<Option::Type, Real>(),
            py::arg("type"), py::arg("strike"));

    py::class_<VanillaSwingOption, OneAssetOption,
               ext::shared_ptr<VanillaSwingOption>>(
        m, "VanillaSwingOption", "Vanilla swing option.")
        .def(py::init<const ext::shared_ptr<Payoff>&,
                      const ext::shared_ptr<SwingExercise>&,
                      Size, Size>(),
            py::arg("payoff"), py::arg("exercise"),
            py::arg("minExerciseRights"), py::arg("maxExerciseRights"),
            "Constructs from payoff, swing exercise, and exercise-right bounds.");
}
