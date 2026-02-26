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
#include <ql/instruments/lookbackoption.hpp>
#include <ql/instruments/payoffs.hpp>
#include <ql/exercise.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::lookbackoption(py::module_& m) {
    // Floating lookback uses FloatingTypePayoff (TypePayoff subclass).
    // TypePayoff is not a pybind11 base, so we use a lambda converting from
    // the registered FloatingTypePayoff shared_ptr.
    py::class_<ContinuousFloatingLookbackOption, OneAssetOption,
               ext::shared_ptr<ContinuousFloatingLookbackOption>>(
        m, "ContinuousFloatingLookbackOption",
        "Continuous floating-strike lookback option.")
        .def(py::init([](Real currentMinmax,
                         const ext::shared_ptr<FloatingTypePayoff>& payoff,
                         const ext::shared_ptr<Exercise>& exercise) {
                 return ext::make_shared<ContinuousFloatingLookbackOption>(
                     currentMinmax, payoff, exercise);
             }),
             py::arg("currentMinmax"),
             py::arg("payoff"),
             py::arg("exercise"));

    py::class_<ContinuousFixedLookbackOption, OneAssetOption,
               ext::shared_ptr<ContinuousFixedLookbackOption>>(
        m, "ContinuousFixedLookbackOption",
        "Continuous fixed-strike lookback option.")
        .def(py::init<Real,
                      const ext::shared_ptr<StrikedTypePayoff>&,
                      const ext::shared_ptr<Exercise>&>(),
             py::arg("currentMinmax"),
             py::arg("payoff"),
             py::arg("exercise"));

    py::class_<ContinuousPartialFloatingLookbackOption,
               ContinuousFloatingLookbackOption,
               ext::shared_ptr<ContinuousPartialFloatingLookbackOption>>(
        m, "ContinuousPartialFloatingLookbackOption",
        "Continuous partial floating-strike lookback option.")
        .def(py::init([](Real currentMinmax, Real lambda, Date lookbackPeriodEnd,
                         const ext::shared_ptr<FloatingTypePayoff>& payoff,
                         const ext::shared_ptr<Exercise>& exercise) {
                 return ext::make_shared<ContinuousPartialFloatingLookbackOption>(
                     currentMinmax, lambda, lookbackPeriodEnd, payoff, exercise);
             }),
             py::arg("currentMinmax"),
             py::arg("lambda"),
             py::arg("lookbackPeriodEnd"),
             py::arg("payoff"),
             py::arg("exercise"));

    py::class_<ContinuousPartialFixedLookbackOption,
               ContinuousFixedLookbackOption,
               ext::shared_ptr<ContinuousPartialFixedLookbackOption>>(
        m, "ContinuousPartialFixedLookbackOption",
        "Continuous partial fixed-strike lookback option.")
        .def(py::init<Date,
                      const ext::shared_ptr<StrikedTypePayoff>&,
                      const ext::shared_ptr<Exercise>&>(),
             py::arg("lookbackPeriodStart"),
             py::arg("payoff"),
             py::arg("exercise"));
}
