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
#include <ql/instruments/doublebarriertype.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::doublebarriertype(py::module_& m) {
    py::enum_<DoubleBarrier::Type>(m, "DoubleBarrierType", "Double barrier type.")
        .value("KnockIn", DoubleBarrier::KnockIn)
        .value("KnockOut", DoubleBarrier::KnockOut)
        .value("KIKO", DoubleBarrier::KIKO, "Lower barrier KI, upper KO.")
        .value("KOKI", DoubleBarrier::KOKI, "Lower barrier KO, upper KI.");
}
