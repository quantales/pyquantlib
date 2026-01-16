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
#include <ql/models/calibrationhelper.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::calibrationhelper(py::module_& m) {
    py::module_ base = m.def_submodule("base", "Abstract base classes");

    py::class_<CalibrationHelper, PyCalibrationHelper,
               ext::shared_ptr<CalibrationHelper>>(
        base, "CalibrationHelper",
        "Abstract base class for model calibration helpers.")
        .def("calibrationError", &CalibrationHelper::calibrationError,
            "Returns the calibration error.");
}
