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
#include "pyquantlib/binding_manager.h"
#include <ql/termstructures/volatility/inflation/yoyinflationoptionletvolatilitystructure.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::yoyinflationoptionletvolatilitystructure(
    py::module_& m) {
    auto base = py::module_::import("pyquantlib.base");

    // YoYOptionletVolatilitySurface ABC (base submodule)
    py::class_<YoYOptionletVolatilitySurface, VolatilityTermStructure,
               ext::shared_ptr<YoYOptionletVolatilitySurface>>(
        base, "YoYOptionletVolatilitySurface",
        "Abstract base class for YoY inflation optionlet volatility.")
        .def("volatility",
            py::overload_cast<const Date&, Rate, const Period&, bool>(
                &YoYOptionletVolatilitySurface::volatility, py::const_),
            py::arg("maturityDate"), py::arg("strike"),
            py::arg("obsLag") = Period(-1, Days),
            py::arg("extrapolate") = false,
            "Returns the volatility for a given maturity date and strike.")
        .def("volatility",
            py::overload_cast<const Period&, Rate, const Period&, bool>(
                &YoYOptionletVolatilitySurface::volatility, py::const_),
            py::arg("optionTenor"), py::arg("strike"),
            py::arg("obsLag") = Period(-1, Days),
            py::arg("extrapolate") = false,
            "Returns the volatility for a given option tenor and strike.")
        .def("totalVariance",
            py::overload_cast<const Date&, Rate, const Period&, bool>(
                &YoYOptionletVolatilitySurface::totalVariance, py::const_),
            py::arg("exerciseDate"), py::arg("strike"),
            py::arg("obsLag") = Period(-1, Days),
            py::arg("extrapolate") = false,
            "Returns the total variance.")
        .def("observationLag",
            &YoYOptionletVolatilitySurface::observationLag,
            "Returns the observation lag.")
        .def("frequency", &YoYOptionletVolatilitySurface::frequency,
            "Returns the frequency.")
        .def("indexIsInterpolated",
            &YoYOptionletVolatilitySurface::indexIsInterpolated,
            "Returns whether the index is interpolated.")
        .def("baseDate", &YoYOptionletVolatilitySurface::baseDate,
            "Returns the base date.")
        .def("baseLevel", &YoYOptionletVolatilitySurface::baseLevel,
            "Returns the base level of volatility.")
        .def("volatilityType",
            &YoYOptionletVolatilitySurface::volatilityType,
            "Returns the volatility type.")
        .def("displacement",
            &YoYOptionletVolatilitySurface::displacement,
            "Returns the displacement for shifted lognormal.");

    // Handle<YoYOptionletVolatilitySurface>
    bindHandle<YoYOptionletVolatilitySurface>(
        m, "YoYOptionletVolatilitySurfaceHandle",
        "Handle to YoYOptionletVolatilitySurface.");
    bindRelinkableHandle<YoYOptionletVolatilitySurface>(
        m, "RelinkableYoYOptionletVolatilitySurfaceHandle",
        "Relinkable handle to YoYOptionletVolatilitySurface.");

    // ConstantYoYOptionletVolatility (concrete, main module)
    py::class_<ConstantYoYOptionletVolatility,
               YoYOptionletVolatilitySurface,
               ext::shared_ptr<ConstantYoYOptionletVolatility>>(
        m, "ConstantYoYOptionletVolatility",
        "Constant YoY inflation optionlet volatility.")
        // Volatility constructor
        .def(py::init<Volatility, Natural, const Calendar&,
                       BusinessDayConvention, const DayCounter&,
                       const Period&, Frequency, bool,
                       Rate, Rate, VolatilityType, Real>(),
            py::arg("volatility"),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("bdc"),
            py::arg("dayCounter"),
            py::arg("observationLag"),
            py::arg("frequency"),
            py::arg("indexIsInterpolated"),
            py::arg("minStrike") = -1.0,
            py::arg("maxStrike") = 100.0,
            py::arg("volatilityType") = VolatilityType::ShiftedLognormal,
            py::arg("displacement") = 0.0,
            "Constructs with a constant volatility value.")
        // Quote constructor
        .def(py::init<Handle<Quote>, Natural, const Calendar&,
                       BusinessDayConvention, const DayCounter&,
                       const Period&, Frequency, bool,
                       Rate, Rate, VolatilityType, Real>(),
            py::arg("volatility"),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("bdc"),
            py::arg("dayCounter"),
            py::arg("observationLag"),
            py::arg("frequency"),
            py::arg("indexIsInterpolated"),
            py::arg("minStrike") = -1.0,
            py::arg("maxStrike") = 100.0,
            py::arg("volatilityType") = VolatilityType::ShiftedLognormal,
            py::arg("displacement") = 0.0,
            "Constructs with a volatility quote.")
        // Hidden handle constructor (from shared_ptr<Quote>)
        .def(py::init([](const ext::shared_ptr<Quote>& vol,
                         Natural settlementDays, const Calendar& cal,
                         BusinessDayConvention bdc, const DayCounter& dc,
                         const Period& obsLag, Frequency freq,
                         bool indexIsInterp,
                         Rate minStrike, Rate maxStrike,
                         VolatilityType volType, Real displacement) {
                return ext::make_shared<ConstantYoYOptionletVolatility>(
                    Handle<Quote>(vol), settlementDays, cal, bdc, dc,
                    obsLag, freq, indexIsInterp,
                    minStrike, maxStrike, volType, displacement);
            }),
            py::arg("volatility"),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("bdc"),
            py::arg("dayCounter"),
            py::arg("observationLag"),
            py::arg("frequency"),
            py::arg("indexIsInterpolated"),
            py::arg("minStrike") = -1.0,
            py::arg("maxStrike") = 100.0,
            py::arg("volatilityType") = VolatilityType::ShiftedLognormal,
            py::arg("displacement") = 0.0,
            "Constructs with a volatility quote (handle created internally).");
}
