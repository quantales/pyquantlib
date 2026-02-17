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
#include <ql/instruments/inflationcapfloor.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/termstructures/inflationtermstructure.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::inflationcapfloor(py::module_& m) {
    // Type enum
    py::enum_<YoYInflationCapFloor::Type>(
        m, "YoYInflationCapFloorType",
        "YoY inflation cap/floor type.")
        .value("Cap", YoYInflationCapFloor::Cap)
        .value("Floor", YoYInflationCapFloor::Floor)
        .value("Collar", YoYInflationCapFloor::Collar);

    // YoYInflationCapFloor
    py::class_<YoYInflationCapFloor, Instrument,
               ext::shared_ptr<YoYInflationCapFloor>>(
        m, "YoYInflationCapFloor",
        "YoY inflation cap, floor, or collar.")
        // Full constructor (cap rates + floor rates)
        .def(py::init<YoYInflationCapFloor::Type,
                       Leg, std::vector<Rate>, std::vector<Rate>>(),
            py::arg("type"),
            py::arg("yoyLeg"),
            py::arg("capRates"),
            py::arg("floorRates"),
            "Constructs a YoY inflation cap/floor/collar.")
        // Strikes-only constructor
        .def(py::init<YoYInflationCapFloor::Type,
                       Leg, const std::vector<Rate>&>(),
            py::arg("type"),
            py::arg("yoyLeg"),
            py::arg("strikes"),
            "Constructs a YoY inflation cap or floor with uniform strikes.")
        // Inspectors
        .def("type", &YoYInflationCapFloor::type,
            "Returns the type.")
        .def("capRates", &YoYInflationCapFloor::capRates,
            "Returns the cap rates.")
        .def("floorRates", &YoYInflationCapFloor::floorRates,
            "Returns the floor rates.")
        .def("yoyLeg", &YoYInflationCapFloor::yoyLeg,
            py::return_value_policy::reference_internal,
            "Returns the YoY leg.")
        .def("startDate", &YoYInflationCapFloor::startDate,
            "Returns the start date.")
        .def("maturityDate", &YoYInflationCapFloor::maturityDate,
            "Returns the maturity date.")
        .def("isExpired", &YoYInflationCapFloor::isExpired,
            "Returns True if expired.")
        .def("lastYoYInflationCoupon",
            &YoYInflationCapFloor::lastYoYInflationCoupon,
            "Returns the last YoY inflation coupon.")
        .def("optionlet", &YoYInflationCapFloor::optionlet,
            py::arg("n"),
            "Returns the n-th optionlet as a single-cashflow cap/floor.")
        .def("atmRate", &YoYInflationCapFloor::atmRate,
            py::arg("discountCurve"),
            "Returns the ATM rate.")
        .def("impliedVolatility", &YoYInflationCapFloor::impliedVolatility,
            py::arg("price"),
            py::arg("yoyCurve"),
            py::arg("guess"),
            py::arg("accuracy") = 1.0e-4,
            py::arg("maxEvaluations") = 100,
            py::arg("minVol") = 1.0e-7,
            py::arg("maxVol") = 4.0,
            "Returns the implied volatility.");

    // YoYInflationCap convenience class
    py::class_<YoYInflationCap, YoYInflationCapFloor,
               ext::shared_ptr<YoYInflationCap>>(
        m, "YoYInflationCap",
        "YoY inflation cap.")
        .def(py::init<const Leg&, const std::vector<Rate>&>(),
            py::arg("yoyLeg"),
            py::arg("exerciseRates"),
            "Constructs a YoY inflation cap.");

    // YoYInflationFloor convenience class
    py::class_<YoYInflationFloor, YoYInflationCapFloor,
               ext::shared_ptr<YoYInflationFloor>>(
        m, "YoYInflationFloor",
        "YoY inflation floor.")
        .def(py::init<const Leg&, const std::vector<Rate>&>(),
            py::arg("yoyLeg"),
            py::arg("exerciseRates"),
            "Constructs a YoY inflation floor.");

    // YoYInflationCollar convenience class
    py::class_<YoYInflationCollar, YoYInflationCapFloor,
               ext::shared_ptr<YoYInflationCollar>>(
        m, "YoYInflationCollar",
        "YoY inflation collar.")
        .def(py::init<const Leg&, const std::vector<Rate>&,
                       const std::vector<Rate>&>(),
            py::arg("yoyLeg"),
            py::arg("capRates"),
            py::arg("floorRates"),
            "Constructs a YoY inflation collar.");
}
