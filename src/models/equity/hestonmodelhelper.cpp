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
#include <ql/models/equity/hestonmodelhelper.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::hestonmodelhelper(py::module_& m) {
    py::class_<HestonModelHelper, BlackCalibrationHelper,
               ext::shared_ptr<HestonModelHelper>>(
        m, "HestonModelHelper",
        "Calibration helper for the Heston model.")
        // Constructor 1: Real s0 (handles)
        .def(py::init<const Period&, Calendar, Real, Real,
                      const Handle<Quote>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<YieldTermStructure>&,
                      BlackCalibrationHelper::CalibrationErrorType>(),
            py::arg("maturity"),
            py::arg("calendar"),
            py::arg("s0"),
            py::arg("strikePrice"),
            py::arg("volatility"),
            py::arg("riskFreeRate"),
            py::arg("dividendYield"),
            py::arg("errorType") = BlackCalibrationHelper::RelativePriceError,
            "Constructs Heston helper with Real spot price.")
        // Constructor 1: Real s0 (hidden handles)
        .def(py::init([](const Period& maturity, const Calendar& calendar,
                        Real s0, Real strikePrice,
                        const ext::shared_ptr<Quote>& volatility,
                        const ext::shared_ptr<YieldTermStructure>& riskFreeRate,
                        const ext::shared_ptr<YieldTermStructure>& dividendYield,
                        BlackCalibrationHelper::CalibrationErrorType errorType) {
            return ext::make_shared<HestonModelHelper>(
                maturity, calendar, s0, strikePrice,
                Handle<Quote>(volatility),
                Handle<YieldTermStructure>(riskFreeRate),
                Handle<YieldTermStructure>(dividendYield),
                errorType);
        }),
            py::arg("maturity"),
            py::arg("calendar"),
            py::arg("s0"),
            py::arg("strikePrice"),
            py::arg("volatility"),
            py::arg("riskFreeRate"),
            py::arg("dividendYield"),
            py::arg("errorType") = BlackCalibrationHelper::RelativePriceError,
            "Constructs Heston helper with Real spot (handles created internally).")
        // Constructor 2: Handle<Quote> s0 (handles)
        .def(py::init<const Period&, Calendar,
                      const Handle<Quote>&, Real,
                      const Handle<Quote>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<YieldTermStructure>&,
                      BlackCalibrationHelper::CalibrationErrorType>(),
            py::arg("maturity"),
            py::arg("calendar"),
            py::arg("s0"),
            py::arg("strikePrice"),
            py::arg("volatility"),
            py::arg("riskFreeRate"),
            py::arg("dividendYield"),
            py::arg("errorType") = BlackCalibrationHelper::RelativePriceError,
            "Constructs Heston helper with Handle<Quote> spot price.")
        // Methods
        .def("modelValue", &HestonModelHelper::modelValue,
            "Returns the model value.")
        .def("blackPrice", &HestonModelHelper::blackPrice,
            py::arg("volatility"),
            "Returns Black price for given volatility.")
        .def("maturity", &HestonModelHelper::maturity,
            "Returns the time to maturity.");
}
