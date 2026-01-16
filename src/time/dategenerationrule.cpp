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
#include <ql/time/dategenerationrule.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_time::dategenerationrule(py::module_& m)
{
    auto pyClassDateGeneration =
        py::class_<QuantLib::DateGeneration>(m, "DateGeneration",
            "Date generation rules for Schedule construction.");

    py::enum_<QuantLib::DateGeneration::Rule>(pyClassDateGeneration, "Rule", py::arithmetic())
        .value("Backward", QuantLib::DateGeneration::Backward,
            "Backward from termination date to effective date.")
        .value("Forward", QuantLib::DateGeneration::Forward,
            "Forward from effective date to termination date.")
        .value("Zero", QuantLib::DateGeneration::Zero,
            "No intermediate dates between effective date and termination date.")
        .value("ThirdWednesday", QuantLib::DateGeneration::ThirdWednesday,
            "All dates but effective/termination are third Wednesday of their month.")
        .value("ThirdWednesdayInclusive", QuantLib::DateGeneration::ThirdWednesdayInclusive,
            "All dates including effective/termination are third Wednesday of their month.")
        .value("Twentieth", QuantLib::DateGeneration::Twentieth,
            "All dates but effective are the twentieth of their month (CDS in emerging markets).")
        .value("TwentiethIMM", QuantLib::DateGeneration::TwentiethIMM,
            "All dates but effective are the twentieth of an IMM month (CDS schedules).")
        .value("OldCDS", QuantLib::DateGeneration::OldCDS,
            "Same as TwentiethIMM with unrestricted date ends (old CDS convention).")
        .value("CDS", QuantLib::DateGeneration::CDS,
            "Credit derivatives standard rule since 'Big Bang' changes in 2009.")
        .value("CDS2015", QuantLib::DateGeneration::CDS2015,
            "Credit derivatives standard rule since December 20th, 2015.")
        .export_values();

    pyClassDateGeneration
        .def(py::init<>())
        ;
}