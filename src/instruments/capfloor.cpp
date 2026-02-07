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
#include <ql/instruments/capfloor.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/termstructures/volatility/volatilitytype.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::capfloor(py::module_& m) {
    // CapFloor::Type enum
    py::enum_<CapFloor::Type>(m, "CapFloorType",
        "Cap/floor type.")
        .value("Cap", CapFloor::Cap)
        .value("Floor", CapFloor::Floor)
        .value("Collar", CapFloor::Collar);

    // CapFloor class
    py::class_<CapFloor, Instrument, ext::shared_ptr<CapFloor>>(
        m, "CapFloor",
        "Interest rate cap, floor, or collar.")
        // Full constructor (cap rates + floor rates)
        .def(py::init<CapFloor::Type, Leg, std::vector<Rate>, std::vector<Rate>>(),
            py::arg("type"),
            py::arg("floatingLeg"),
            py::arg("capRates"),
            py::arg("floorRates"),
            "Constructs a cap/floor/collar.")
        // Strikes-only constructor
        .def(py::init<CapFloor::Type, Leg, const std::vector<Rate>&>(),
            py::arg("type"),
            py::arg("floatingLeg"),
            py::arg("strikes"),
            "Constructs a cap or floor with uniform strikes.")
        // Inspectors
        .def("type", &CapFloor::type,
            "Returns the cap/floor type.")
        .def("capRates", &CapFloor::capRates,
            "Returns the cap rates.")
        .def("floorRates", &CapFloor::floorRates,
            "Returns the floor rates.")
        .def("floatingLeg", &CapFloor::floatingLeg,
            "Returns the floating leg.")
        .def("startDate", &CapFloor::startDate,
            "Returns the start date.")
        .def("maturityDate", &CapFloor::maturityDate,
            "Returns the maturity date.")
        .def("isExpired", &CapFloor::isExpired,
            "Returns True if expired.")
        // ATM rate
        .def("atmRate", &CapFloor::atmRate,
            py::arg("discountCurve"),
            "Returns the ATM rate.")
        // Implied volatility
        .def("impliedVolatility", &CapFloor::impliedVolatility,
            py::arg("price"),
            py::arg("discountCurve"),
            py::arg("guess"),
            py::arg("accuracy") = 1.0e-4,
            py::arg("maxEvaluations") = 100,
            py::arg("minVol") = 1.0e-7,
            py::arg("maxVol") = 4.0,
            py::arg("type") = VolatilityType::ShiftedLognormal,
            py::arg("displacement") = 0.0,
            "Returns the implied volatility.");

    // Cap convenience class
    py::class_<Cap, CapFloor, ext::shared_ptr<Cap>>(
        m, "Cap",
        "Interest rate cap.")
        .def(py::init<const Leg&, const std::vector<Rate>&>(),
            py::arg("floatingLeg"),
            py::arg("exerciseRates"),
            "Constructs a cap.");

    // Floor convenience class
    py::class_<Floor, CapFloor, ext::shared_ptr<Floor>>(
        m, "Floor",
        "Interest rate floor.")
        .def(py::init<const Leg&, const std::vector<Rate>&>(),
            py::arg("floatingLeg"),
            py::arg("exerciseRates"),
            "Constructs a floor.");

    // Collar convenience class
    py::class_<Collar, CapFloor, ext::shared_ptr<Collar>>(
        m, "Collar",
        "Interest rate collar.")
        .def(py::init<const Leg&, const std::vector<Rate>&, const std::vector<Rate>&>(),
            py::arg("floatingLeg"),
            py::arg("capRates"),
            py::arg("floorRates"),
            "Constructs a collar.");
}
