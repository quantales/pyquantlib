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
#include <ql/instruments/asianoption.hpp>
#include <ql/instruments/averagetype.hpp>
#include <ql/exercise.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::asianoption(py::module_& m) {
    py::class_<ContinuousAveragingAsianOption, OneAssetOption,
               ext::shared_ptr<ContinuousAveragingAsianOption>>(
        m, "ContinuousAveragingAsianOption",
        "Continuous-averaging Asian option.")
        .def(py::init<Average::Type,
                       const ext::shared_ptr<StrikedTypePayoff>&,
                       const ext::shared_ptr<Exercise>&>(),
            py::arg("averageType"),
            py::arg("payoff"),
            py::arg("exercise"),
            "Constructs ContinuousAveragingAsianOption.");

    py::class_<DiscreteAveragingAsianOption, OneAssetOption,
               ext::shared_ptr<DiscreteAveragingAsianOption>>(
        m, "DiscreteAveragingAsianOption",
        "Discrete-averaging Asian option.")
        // Constructor with running accumulator and past fixings
        .def(py::init<Average::Type, Real, Size, std::vector<Date>,
                       const ext::shared_ptr<StrikedTypePayoff>&,
                       const ext::shared_ptr<Exercise>&>(),
            py::arg("averageType"),
            py::arg("runningAccumulator"),
            py::arg("pastFixings"),
            py::arg("fixingDates"),
            py::arg("payoff"),
            py::arg("exercise"),
            "Constructs with running accumulator and past fixings count.")
        // Constructor with all fixing dates (unseasoned by default)
        .def(py::init<Average::Type, std::vector<Date>,
                       const ext::shared_ptr<StrikedTypePayoff>&,
                       const ext::shared_ptr<Exercise>&,
                       std::vector<Real>>(),
            py::arg("averageType"),
            py::arg("fixingDates"),
            py::arg("payoff"),
            py::arg("exercise"),
            py::arg("allPastFixings") = std::vector<Real>(),
            "Constructs with all fixing dates.");
}
