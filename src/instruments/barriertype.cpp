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
#include <ql/instruments/barriertype.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::barriertype(py::module_& m) {
    py::enum_<Barrier::Type>(m, "BarrierType", "Barrier type.")
        .value("DownIn", Barrier::DownIn)
        .value("UpIn", Barrier::UpIn)
        .value("DownOut", Barrier::DownOut)
        .value("UpOut", Barrier::UpOut);
}
