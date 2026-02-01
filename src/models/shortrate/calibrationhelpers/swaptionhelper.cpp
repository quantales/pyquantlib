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
#include <ql/models/shortrate/calibrationhelpers/swaptionhelper.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::swaptionhelper(py::module_& m) {
    // RateAveraging enum
    py::class_<RateAveraging> rateAvgClass(m, "RateAveraging",
        "Rate averaging methods for multi-fixing coupons.");

    py::enum_<RateAveraging::Type>(rateAvgClass, "Type",
        "Rate averaging type.")
        .value("Simple", RateAveraging::Simple,
            "Simple averaging: sum of sub-period interest amounts.")
        .value("Compound", RateAveraging::Compound,
            "Compound averaging: compounded sub-period rates.");

    // SwaptionHelper
    py::class_<SwaptionHelper, BlackCalibrationHelper,
               ext::shared_ptr<SwaptionHelper>>(
        m, "SwaptionHelper",
        "Calibration helper for interest-rate swaptions.")
        // Constructor 1: Period maturity, Period length (handles)
        .def(py::init<const Period&, const Period&, const Handle<Quote>&,
                      ext::shared_ptr<IborIndex>, const Period&,
                      DayCounter, DayCounter, Handle<YieldTermStructure>,
                      BlackCalibrationHelper::CalibrationErrorType,
                      Real, Real, VolatilityType, Real, Natural,
                      RateAveraging::Type>(),
            py::arg("maturity"),
            py::arg("length"),
            py::arg("volatility"),
            py::arg("index"),
            py::arg("fixedLegTenor"),
            py::arg("fixedLegDayCounter"),
            py::arg("floatingLegDayCounter"),
            py::arg("termStructure"),
            py::arg("errorType") = BlackCalibrationHelper::RelativePriceError,
            py::arg("strike") = Null<Real>(),
            py::arg("nominal") = 1.0,
            py::arg("type") = ShiftedLognormal,
            py::arg("shift") = 0.0,
            py::arg("settlementDays") = Null<Size>(),
            py::arg("averagingMethod") = RateAveraging::Compound,
            "Constructs swaption helper with period maturity and length.")
        // Constructor 1: Period maturity, Period length (hidden handles)
        .def(py::init([](const Period& maturity, const Period& length,
                        const ext::shared_ptr<Quote>& volatility,
                        const ext::shared_ptr<IborIndex>& index,
                        const Period& fixedLegTenor,
                        const DayCounter& fixedLegDayCounter,
                        const DayCounter& floatingLegDayCounter,
                        const ext::shared_ptr<YieldTermStructure>& termStructure,
                        BlackCalibrationHelper::CalibrationErrorType errorType,
                        Real strike, Real nominal, VolatilityType type,
                        Real shift, Natural settlementDays,
                        RateAveraging::Type averagingMethod) {
            return ext::make_shared<SwaptionHelper>(
                maturity, length, Handle<Quote>(volatility), index,
                fixedLegTenor, fixedLegDayCounter, floatingLegDayCounter,
                Handle<YieldTermStructure>(termStructure),
                errorType, strike, nominal, type, shift, settlementDays,
                averagingMethod);
        }),
            py::arg("maturity"),
            py::arg("length"),
            py::arg("volatility"),
            py::arg("index"),
            py::arg("fixedLegTenor"),
            py::arg("fixedLegDayCounter"),
            py::arg("floatingLegDayCounter"),
            py::arg("termStructure"),
            py::arg("errorType") = BlackCalibrationHelper::RelativePriceError,
            py::arg("strike") = Null<Real>(),
            py::arg("nominal") = 1.0,
            py::arg("type") = ShiftedLognormal,
            py::arg("shift") = 0.0,
            py::arg("settlementDays") = Null<Size>(),
            py::arg("averagingMethod") = RateAveraging::Compound,
            "Constructs swaption helper from period maturity and length.")
        // Constructor 2: Date exercise, Period length (handles)
        .def(py::init<const Date&, const Period&, const Handle<Quote>&,
                      ext::shared_ptr<IborIndex>, const Period&,
                      DayCounter, DayCounter, Handle<YieldTermStructure>,
                      BlackCalibrationHelper::CalibrationErrorType,
                      Real, Real, VolatilityType, Real, Natural,
                      RateAveraging::Type>(),
            py::arg("exerciseDate"),
            py::arg("length"),
            py::arg("volatility"),
            py::arg("index"),
            py::arg("fixedLegTenor"),
            py::arg("fixedLegDayCounter"),
            py::arg("floatingLegDayCounter"),
            py::arg("termStructure"),
            py::arg("errorType") = BlackCalibrationHelper::RelativePriceError,
            py::arg("strike") = Null<Real>(),
            py::arg("nominal") = 1.0,
            py::arg("type") = ShiftedLognormal,
            py::arg("shift") = 0.0,
            py::arg("settlementDays") = Null<Size>(),
            py::arg("averagingMethod") = RateAveraging::Compound,
            "Constructs swaption helper with exercise date and swap length.")
        // Constructor 2: Date exercise, Period length (hidden handles)
        .def(py::init([](const Date& exerciseDate, const Period& length,
                        const ext::shared_ptr<Quote>& volatility,
                        const ext::shared_ptr<IborIndex>& index,
                        const Period& fixedLegTenor,
                        const DayCounter& fixedLegDayCounter,
                        const DayCounter& floatingLegDayCounter,
                        const ext::shared_ptr<YieldTermStructure>& termStructure,
                        BlackCalibrationHelper::CalibrationErrorType errorType,
                        Real strike, Real nominal, VolatilityType type,
                        Real shift, Natural settlementDays,
                        RateAveraging::Type averagingMethod) {
            return ext::make_shared<SwaptionHelper>(
                exerciseDate, length, Handle<Quote>(volatility), index,
                fixedLegTenor, fixedLegDayCounter, floatingLegDayCounter,
                Handle<YieldTermStructure>(termStructure),
                errorType, strike, nominal, type, shift, settlementDays,
                averagingMethod);
        }),
            py::arg("exerciseDate"),
            py::arg("length"),
            py::arg("volatility"),
            py::arg("index"),
            py::arg("fixedLegTenor"),
            py::arg("fixedLegDayCounter"),
            py::arg("floatingLegDayCounter"),
            py::arg("termStructure"),
            py::arg("errorType") = BlackCalibrationHelper::RelativePriceError,
            py::arg("strike") = Null<Real>(),
            py::arg("nominal") = 1.0,
            py::arg("type") = ShiftedLognormal,
            py::arg("shift") = 0.0,
            py::arg("settlementDays") = Null<Size>(),
            py::arg("averagingMethod") = RateAveraging::Compound,
            "Constructs swaption helper from exercise date and swap length.")
        // Constructor 3: Date exercise, Date end (handles)
        .def(py::init<const Date&, const Date&, const Handle<Quote>&,
                      ext::shared_ptr<IborIndex>, const Period&,
                      DayCounter, DayCounter, Handle<YieldTermStructure>,
                      BlackCalibrationHelper::CalibrationErrorType,
                      Real, Real, VolatilityType, Real, Natural,
                      RateAveraging::Type>(),
            py::arg("exerciseDate"),
            py::arg("endDate"),
            py::arg("volatility"),
            py::arg("index"),
            py::arg("fixedLegTenor"),
            py::arg("fixedLegDayCounter"),
            py::arg("floatingLegDayCounter"),
            py::arg("termStructure"),
            py::arg("errorType") = BlackCalibrationHelper::RelativePriceError,
            py::arg("strike") = Null<Real>(),
            py::arg("nominal") = 1.0,
            py::arg("type") = ShiftedLognormal,
            py::arg("shift") = 0.0,
            py::arg("settlementDays") = Null<Size>(),
            py::arg("averagingMethod") = RateAveraging::Compound,
            "Constructs swaption helper with exercise and end dates.")
        // Constructor 3: Date exercise, Date end (hidden handles)
        .def(py::init([](const Date& exerciseDate, const Date& endDate,
                        const ext::shared_ptr<Quote>& volatility,
                        const ext::shared_ptr<IborIndex>& index,
                        const Period& fixedLegTenor,
                        const DayCounter& fixedLegDayCounter,
                        const DayCounter& floatingLegDayCounter,
                        const ext::shared_ptr<YieldTermStructure>& termStructure,
                        BlackCalibrationHelper::CalibrationErrorType errorType,
                        Real strike, Real nominal, VolatilityType type,
                        Real shift, Natural settlementDays,
                        RateAveraging::Type averagingMethod) {
            return ext::make_shared<SwaptionHelper>(
                exerciseDate, endDate, Handle<Quote>(volatility), index,
                fixedLegTenor, fixedLegDayCounter, floatingLegDayCounter,
                Handle<YieldTermStructure>(termStructure),
                errorType, strike, nominal, type, shift, settlementDays,
                averagingMethod);
        }),
            py::arg("exerciseDate"),
            py::arg("endDate"),
            py::arg("volatility"),
            py::arg("index"),
            py::arg("fixedLegTenor"),
            py::arg("fixedLegDayCounter"),
            py::arg("floatingLegDayCounter"),
            py::arg("termStructure"),
            py::arg("errorType") = BlackCalibrationHelper::RelativePriceError,
            py::arg("strike") = Null<Real>(),
            py::arg("nominal") = 1.0,
            py::arg("type") = ShiftedLognormal,
            py::arg("shift") = 0.0,
            py::arg("settlementDays") = Null<Size>(),
            py::arg("averagingMethod") = RateAveraging::Compound,
            "Constructs swaption helper from exercise and end dates.")
        // Methods
        .def("modelValue", &SwaptionHelper::modelValue,
            "Returns the model value.")
        .def("blackPrice", &SwaptionHelper::blackPrice,
            py::arg("volatility"),
            "Returns Black price for given volatility.")
        .def("underlying", &SwaptionHelper::underlying,
            py::return_value_policy::reference_internal,
            "Returns the underlying swap.")
        .def("swaption", &SwaptionHelper::swaption,
            "Returns the swaption instrument.");
}
