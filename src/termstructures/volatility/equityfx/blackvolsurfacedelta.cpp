/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2026 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/termstructures/volatility/equityfx/blackvolsurfacedelta.hpp>
#include <ql/termstructures/volatility/equityfx/blackvoltimeextrapolation.hpp>
#include <ql/quotes/deltavolquote.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/math/matrix.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::blackvolsurfacedelta(py::module_& m) {
    auto cls = py::class_<BlackVolatilitySurfaceDelta, BlackVolatilityTermStructure,
                          ext::shared_ptr<BlackVolatilitySurfaceDelta>>(
        m, "BlackVolatilitySurfaceDelta",
        "Black volatility surface parameterized by FX market deltas.");

    py::enum_<BlackVolatilitySurfaceDelta::SmileInterpolationMethod>(
        cls, "SmileInterpolationMethod", "Per-expiry smile interpolation method.")
        .value("Linear", BlackVolatilitySurfaceDelta::SmileInterpolationMethod::Linear)
        .value("NaturalCubic", BlackVolatilitySurfaceDelta::SmileInterpolationMethod::NaturalCubic)
        .value("FinancialCubic", BlackVolatilitySurfaceDelta::SmileInterpolationMethod::FinancialCubic)
        .value("CubicSpline", BlackVolatilitySurfaceDelta::SmileInterpolationMethod::CubicSpline);

    cls
        .def(py::init<Date, const std::vector<Date>&, const std::vector<Real>&,
                      const std::vector<Real>&, bool, const Matrix&, const DayCounter&,
                      const Calendar&, const Handle<Quote>&,
                      const Handle<YieldTermStructure>&, const Handle<YieldTermStructure>&,
                      DeltaVolQuote::DeltaType, DeltaVolQuote::AtmType,
                      std::optional<DeltaVolQuote::DeltaType>,
                      BlackVolatilitySurfaceDelta::SmileInterpolationMethod, bool,
                      BlackVolTimeExtrapolation::Type, const Period&,
                      DeltaVolQuote::DeltaType, DeltaVolQuote::AtmType,
                      std::optional<DeltaVolQuote::DeltaType>>(),
            py::arg("referenceDate"),
            py::arg("dates"),
            py::arg("putDeltas"),
            py::arg("callDeltas"),
            py::arg("hasAtm"),
            py::arg("blackVolMatrix"),
            py::arg("dayCounter"),
            py::arg("calendar"),
            py::arg("spot"),
            py::arg("domesticTS"),
            py::arg("foreignTS"),
            py::arg("deltaType") = DeltaVolQuote::Spot,
            py::arg("atmType") = DeltaVolQuote::AtmDeltaNeutral,
            py::arg("atmDeltaType") = py::none(),
            py::arg("interpolationMethod") =
                BlackVolatilitySurfaceDelta::SmileInterpolationMethod::Linear,
            py::arg("flatStrikeExtrapolation") = false,
            py::arg("timeExtrapolationType") = BlackVolTimeExtrapolation::FlatVolatility,
            py::arg("switchTenor") = Period(0, Days),
            py::arg("longTermDeltaType") = DeltaVolQuote::Fwd,
            py::arg("longTermAtmType") = DeltaVolQuote::AtmDeltaNeutral,
            py::arg("longTermAtmDeltaType") = py::none(),
            "Constructs from a grid of expiry dates and delta quotes. The spot, "
            "domestic, and foreign handles are used to convert deltas to strikes.")
        .def("dates", &BlackVolatilitySurfaceDelta::dates,
            py::return_value_policy::reference_internal,
            "Returns the expiry dates.")
        .def("blackVolSmile",
            py::overload_cast<Time>(&BlackVolatilitySurfaceDelta::blackVolSmile, py::const_),
            py::arg("t"),
            "Returns the Black vol smile section at time t (year fraction).")
        .def("blackVolSmile",
            py::overload_cast<const Date&>(&BlackVolatilitySurfaceDelta::blackVolSmile, py::const_),
            py::arg("date"),
            "Returns the Black vol smile section at the given expiry date.");
}
