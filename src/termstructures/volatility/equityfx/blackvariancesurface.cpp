/*
 * PyQuantLib: Python bindings for QuantLib
 * Copyright (c) 2025 Yassine Idyiahia
 *
 * QuantLib is Copyright (c) 2000-2025 The QuantLib Authors
 * QuantLib is free software under a modified BSD license.
 * See http://quantlib.org/ for more information.
 *
 * Source: https://github.com/quantales/pyquantlib
 * Licensed under the BSD 3-Clause License. See LICENSE file for details.
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/termstructures/volatility/equityfx/blackvariancesurface.hpp>
#include <ql/math/interpolations/bilinearinterpolation.hpp>
#include <ql/math/interpolations/bicubicsplineinterpolation.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <algorithm>
#include <cctype>

namespace py = pybind11;
using namespace QuantLib;

namespace {
    std::string toLower(std::string s) {
        std::transform(s.begin(), s.end(), s.begin(),
                       [](unsigned char c) { return std::tolower(c); });
        return s;
    }
}

void ql_termstructures::blackvariancesurface(py::module_& m) {
    // Extrapolation enum
    py::enum_<BlackVarianceSurface::Extrapolation>(m, "BlackVarianceSurfaceExtrapolation",
        "Extrapolation type for BlackVarianceSurface.")
        .value("ConstantExtrapolation", BlackVarianceSurface::ConstantExtrapolation)
        .value("InterpolatorDefaultExtrapolation",
               BlackVarianceSurface::InterpolatorDefaultExtrapolation);

    py::class_<BlackVarianceSurface, BlackVarianceTermStructure,
               ext::shared_ptr<BlackVarianceSurface>>(
        m, "BlackVarianceSurface",
        "Black volatility surface modelled as a variance surface.")
        .def(py::init<const Date&, const Calendar&, const std::vector<Date>&,
                      std::vector<Real>, const Matrix&, DayCounter,
                      BlackVarianceSurface::Extrapolation,
                      BlackVarianceSurface::Extrapolation>(),
            py::arg("referenceDate"),
            py::arg("calendar"),
            py::arg("dates"),
            py::arg("strikes"),
            py::arg("blackVolMatrix"),
            py::arg("dayCounter"),
            py::arg("lowerExtrapolation") = BlackVarianceSurface::InterpolatorDefaultExtrapolation,
            py::arg("upperExtrapolation") = BlackVarianceSurface::InterpolatorDefaultExtrapolation,
            "Constructs from date/strike grid and volatility matrix.")
        .def("dayCounter", &BlackVarianceSurface::dayCounter,
            "Returns the day counter.")
        .def("maxDate", &BlackVarianceSurface::maxDate,
            "Returns the maximum date.")
        .def("minStrike", &BlackVarianceSurface::minStrike,
            "Returns the minimum strike.")
        .def("maxStrike", &BlackVarianceSurface::maxStrike,
            "Returns the maximum strike.")
        .def("setInterpolation",
            [](BlackVarianceSurface& self, const std::string& interpolator) {
                std::string s = toLower(interpolator);
                if (s == "bilinear") {
                    self.setInterpolation<Bilinear>();
                } else if (s == "bicubic") {
                    self.setInterpolation<Bicubic>();
                } else {
                    throw std::invalid_argument(
                        "Unknown interpolator: " + interpolator +
                        ". Supported: 'bilinear', 'bicubic'");
                }
            },
            py::arg("interpolator"),
            "Sets interpolation method. Supported: 'bilinear', 'bicubic'.");
}
