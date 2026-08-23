/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/instruments/perpetualfutures.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::perpetualfutures(py::module_& m) {
    py::class_<PerpetualFutures, Instrument, ext::shared_ptr<PerpetualFutures>>
        cls(m, "PerpetualFutures",
            "Perpetual future with periodic funding payments.");

    py::enum_<PerpetualFutures::PayoffType>(cls, "PayoffType",
        "Currency in which margin and settlement are made.")
        .value("Linear", PerpetualFutures::Linear,
               "Margin and settlement in the domestic currency.")
        .value("Inverse", PerpetualFutures::Inverse,
               "Margin and settlement in the foreign currency.")
        .value("Quanto", PerpetualFutures::Quanto,
               "Margin and settlement in a third currency.")
        .export_values();

    py::enum_<PerpetualFutures::FundingType>(cls, "FundingType",
        "Spot used when accruing the funding payment.")
        .value("FundingWithPreviousSpot",
               PerpetualFutures::FundingWithPreviousSpot,
               "Funding accrues against the previous spot.")
        .value("FundingWithCurrentSpot",
               PerpetualFutures::FundingWithCurrentSpot,
               "Funding accrues against the current spot.")
        .export_values();

    cls.def(py::init<PerpetualFutures::PayoffType, PerpetualFutures::FundingType,
                     Period, Calendar, DayCounter>(),
            py::arg("payoffType"),
            py::arg("fundingType") = PerpetualFutures::FundingWithCurrentSpot,
            py::arg("fundingFrequency") = Period(8, Hours),
            py::arg("calendar") = NullCalendar(),
            py::arg("dayCounter") = ActualActual(ActualActual::ISDA),
            "Constructs a perpetual future.");
}
