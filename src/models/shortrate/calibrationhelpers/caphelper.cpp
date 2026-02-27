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
#include <ql/models/shortrate/calibrationhelpers/caphelper.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::caphelper(py::module_& m) {
    py::class_<CapHelper, BlackCalibrationHelper,
               ext::shared_ptr<CapHelper>>(
        m, "CapHelper",
        "Calibration helper for ATM caps.")
        // Handle constructor
        .def(py::init<const Period&, const Handle<Quote>&,
                      ext::shared_ptr<IborIndex>, Frequency,
                      DayCounter, bool, Handle<YieldTermStructure>,
                      BlackCalibrationHelper::CalibrationErrorType,
                      VolatilityType, Real>(),
            py::arg("length"),
            py::arg("volatility"),
            py::arg("index"),
            py::arg("fixedLegFrequency"),
            py::arg("fixedLegDayCounter"),
            py::arg("includeFirstSwaplet"),
            py::arg("termStructure"),
            py::arg("errorType") = BlackCalibrationHelper::RelativePriceError,
            py::arg("type") = ShiftedLognormal,
            py::arg("shift") = 0.0,
            "Constructs cap helper with handles.")
        // Hidden handle constructor
        .def(py::init([](const Period& length,
                        const ext::shared_ptr<Quote>& volatility,
                        const ext::shared_ptr<IborIndex>& index,
                        Frequency fixedLegFrequency,
                        const DayCounter& fixedLegDayCounter,
                        bool includeFirstSwaplet,
                        const ext::shared_ptr<YieldTermStructure>& termStructure,
                        BlackCalibrationHelper::CalibrationErrorType errorType,
                        VolatilityType type, Real shift) {
            return ext::make_shared<CapHelper>(
                length, Handle<Quote>(volatility), index,
                fixedLegFrequency, fixedLegDayCounter, includeFirstSwaplet,
                Handle<YieldTermStructure>(termStructure),
                errorType, type, shift);
        }),
            py::arg("length"),
            py::arg("volatility"),
            py::arg("index"),
            py::arg("fixedLegFrequency"),
            py::arg("fixedLegDayCounter"),
            py::arg("includeFirstSwaplet"),
            py::arg("termStructure"),
            py::arg("errorType") = BlackCalibrationHelper::RelativePriceError,
            py::arg("type") = ShiftedLognormal,
            py::arg("shift") = 0.0,
            "Constructs cap helper (handles created internally).")
        .def("modelValue", &CapHelper::modelValue,
            "Returns the model value.")
        .def("blackPrice", &CapHelper::blackPrice,
            py::arg("volatility"),
            "Returns Black price for given volatility.");
}
