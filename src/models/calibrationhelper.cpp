/*
 * PyQuantLib: Python bindings for QuantLib
 * Copyright (c) 2025 Yassine Idyiahia
 *
 * QuantLib is Copyright (c) 2000-2025 The QuantLib Authors
 * QuantLib is free software under a modified BSD license.
 * See http://quantlib.org/ for more information.
 *
 * Source: https://github.com/quantales/pyquantlib
 * Licensed under the BSD 3-Clause License. See LICENSE file for details.
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
