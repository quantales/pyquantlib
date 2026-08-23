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
#include <ql/termstructures/volatility/equityfx/piecewiseblackvariancesurface.hpp>
#include <ql/termstructures/volatility/smilesection.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::piecewiseblackvariancesurface(py::module_& m) {
    py::class_<PiecewiseBlackVarianceSurface, BlackVarianceTermStructure,
               ext::shared_ptr<PiecewiseBlackVarianceSurface>>(
        m, "PiecewiseBlackVarianceSurface",
        "Black volatility surface built from one smile section per tenor, "
        "interpolated linearly in total variance between tenors.")
        .def(py::init<const Date&, const std::vector<Date>&,
                      std::vector<ext::shared_ptr<SmileSection>>,
                      DayCounter>(),
             py::arg("referenceDate"),
             py::arg("dates"),
             py::arg("smileSections"),
             py::arg("dayCounter"),
             "Constructs from one smile section per date.")
        .def(py::init<const Date&, const Date&, ext::shared_ptr<SmileSection>,
                      DayCounter>(),
             py::arg("referenceDate"),
             py::arg("date"),
             py::arg("smileSection"),
             py::arg("dayCounter"),
             "Constructs from a single smile section.")
        .def_static("makeFromGrid", &PiecewiseBlackVarianceSurface::makeFromGrid,
                    py::arg("referenceDate"),
                    py::arg("dates"),
                    py::arg("strikes"),
                    py::arg("blackVols"),
                    py::arg("dayCounter"),
                    "Builds the surface from a rectangular grid of Black "
                    "volatilities, with rows indexed by strike and columns by "
                    "date.")
        .def("dayCounter", &PiecewiseBlackVarianceSurface::dayCounter,
             "Returns the day counter.")
        .def("maxDate", &PiecewiseBlackVarianceSurface::maxDate,
             "Returns the latest date for which the surface is defined.")
        .def("minStrike", &PiecewiseBlackVarianceSurface::minStrike,
             "Returns the minimum strike.")
        .def("maxStrike", &PiecewiseBlackVarianceSurface::maxStrike,
             "Returns the maximum strike.");
}
