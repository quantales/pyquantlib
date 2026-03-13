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
#include <ql/instruments/partialtimebarrieroption.hpp>
#include <ql/exercise.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::partialtimebarrieroption(py::module_& m) {
    py::enum_<PartialBarrier::Range>(m, "PartialBarrierRange",
        "Time range for partial-time barrier monitoring.")
        .value("Start", PartialBarrier::Start,
            "Monitor from start until cover event.")
        .value("EndB1", PartialBarrier::EndB1,
            "Monitor from cover event to exercise; knock-out on any crossing.")
        .value("EndB2", PartialBarrier::EndB2,
            "Monitor from cover event to exercise; immediate knock-out if wrong side.")
        .export_values();

    py::class_<PartialTimeBarrierOption, OneAssetOption,
               ext::shared_ptr<PartialTimeBarrierOption>>(
        m, "PartialTimeBarrierOption",
        "Partial-time barrier option.")
        .def(py::init<Barrier::Type, PartialBarrier::Range,
                      Real, Real, Date,
                      const ext::shared_ptr<StrikedTypePayoff>&,
                      const ext::shared_ptr<Exercise>&>(),
            py::arg("barrierType"),
            py::arg("barrierRange"),
            py::arg("barrier"),
            py::arg("rebate"),
            py::arg("coverEventDate"),
            py::arg("payoff"),
            py::arg("exercise"),
            "Constructs a partial-time barrier option.");
}
