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
#include <ql/pricingengine.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::calibrationhelper(py::module_& m) {
    py::module_ base = m.def_submodule("base", "Abstract base classes");

    // CalibrationHelper ABC
    py::class_<CalibrationHelper, PyCalibrationHelper,
               ext::shared_ptr<CalibrationHelper>>(
        base, "CalibrationHelper",
        "Abstract base class for model calibration helpers.")
        .def("calibrationError", &CalibrationHelper::calibrationError,
            "Returns the calibration error.");

    // CalibrationErrorType enum
    py::enum_<BlackCalibrationHelper::CalibrationErrorType>(m, "CalibrationErrorType",
        "Type of calibration error calculation.")
        .value("RelativePriceError", BlackCalibrationHelper::RelativePriceError)
        .value("PriceError", BlackCalibrationHelper::PriceError)
        .value("ImpliedVolError", BlackCalibrationHelper::ImpliedVolError);

    // BlackCalibrationHelper ABC
    py::class_<BlackCalibrationHelper, CalibrationHelper, LazyObject,
               ext::shared_ptr<BlackCalibrationHelper>>(
        base, "BlackCalibrationHelper",
        "Base class for Black76-based calibration helpers.")
        .def("volatility", &BlackCalibrationHelper::volatility,
            "Returns the volatility handle.")
        .def("volatilityType", &BlackCalibrationHelper::volatilityType,
            "Returns the volatility type.")
        .def("marketValue", &BlackCalibrationHelper::marketValue,
            "Returns the market value from quoted volatility.")
        .def("modelValue", &BlackCalibrationHelper::modelValue,
            "Returns the model value.")
        .def("calibrationError", &BlackCalibrationHelper::calibrationError,
            "Returns the calibration error.")
        .def("impliedVolatility", &BlackCalibrationHelper::impliedVolatility,
            py::arg("targetValue"),
            py::arg("accuracy") = 1e-4,
            py::arg("maxEvaluations") = 100,
            py::arg("minVol") = 1e-7,
            py::arg("maxVol") = 4.0,
            "Returns implied Black volatility.")
        .def("blackPrice", &BlackCalibrationHelper::blackPrice,
            py::arg("volatility"),
            "Returns Black price for given volatility.")
        .def("setPricingEngine", &BlackCalibrationHelper::setPricingEngine,
            py::arg("engine"),
            "Sets the pricing engine.");
}
