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
#include <ql/termstructures/volatility/equityfx/fixedlocalvolsurface.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

namespace {
    // Helper to convert nested Python lists to shared_ptr vector format
    std::vector<ext::shared_ptr<std::vector<Real>>>
    convertNestedList(const std::vector<std::vector<Real>>& nested_list) {
        std::vector<ext::shared_ptr<std::vector<Real>>> result;
        result.reserve(nested_list.size());
        for (const auto& inner_vec : nested_list) {
            result.push_back(ext::make_shared<std::vector<Real>>(inner_vec));
        }
        return result;
    }
}

void ql_termstructures::fixedlocalvolsurface(py::module_& m) {
    // Extrapolation enum
    py::enum_<FixedLocalVolSurface::Extrapolation>(m, "FixedLocalVolExtrapolation",
        "Extrapolation type for FixedLocalVolSurface.")
        .value("ConstantExtrapolation", FixedLocalVolSurface::ConstantExtrapolation)
        .value("InterpolatorDefaultExtrapolation",
               FixedLocalVolSurface::InterpolatorDefaultExtrapolation);

    py::class_<FixedLocalVolSurface, LocalVolTermStructure,
               ext::shared_ptr<FixedLocalVolSurface>>(
        m, "FixedLocalVolSurface",
        "Fixed local volatility surface with strike/time grid.")
        // With dates
        .def(py::init<const Date&, const std::vector<Date>&, const std::vector<Real>&,
                      ext::shared_ptr<Matrix>, const DayCounter&,
                      FixedLocalVolSurface::Extrapolation,
                      FixedLocalVolSurface::Extrapolation>(),
            py::arg("referenceDate"),
            py::arg("dates"),
            py::arg("strikes"),
            py::arg("localVolMatrix"),
            py::arg("dayCounter"),
            py::arg("lowerExtrapolation") = FixedLocalVolSurface::ConstantExtrapolation,
            py::arg("upperExtrapolation") = FixedLocalVolSurface::ConstantExtrapolation,
            "Constructs from dates and uniform strikes.")
        // With times and uniform strikes
        .def(py::init<const Date&, const std::vector<Time>&, const std::vector<Real>&,
                      ext::shared_ptr<Matrix>, const DayCounter&,
                      FixedLocalVolSurface::Extrapolation,
                      FixedLocalVolSurface::Extrapolation>(),
            py::arg("referenceDate"),
            py::arg("times"),
            py::arg("strikes"),
            py::arg("localVolMatrix"),
            py::arg("dayCounter"),
            py::arg("lowerExtrapolation") = FixedLocalVolSurface::ConstantExtrapolation,
            py::arg("upperExtrapolation") = FixedLocalVolSurface::ConstantExtrapolation,
            "Constructs from times and uniform strikes.")
        // With times and varying strikes per time point
        .def(py::init([](const Date& referenceDate,
                         const std::vector<Time>& times,
                         const std::vector<std::vector<Real>>& strikes_nested,
                         ext::shared_ptr<Matrix> localVolMatrix,
                         const DayCounter& dayCounter,
                         FixedLocalVolSurface::Extrapolation lowerExtrapolation,
                         FixedLocalVolSurface::Extrapolation upperExtrapolation) {
                auto strikes_shared = convertNestedList(strikes_nested);
                return new FixedLocalVolSurface(referenceDate, times, strikes_shared,
                                                localVolMatrix, dayCounter,
                                                lowerExtrapolation, upperExtrapolation);
            }),
            py::arg("referenceDate"),
            py::arg("times"),
            py::arg("strikes"),
            py::arg("localVolMatrix"),
            py::arg("dayCounter"),
            py::arg("lowerExtrapolation") = FixedLocalVolSurface::ConstantExtrapolation,
            py::arg("upperExtrapolation") = FixedLocalVolSurface::ConstantExtrapolation,
            "Constructs from times and varying strikes per time point.")
        .def("maxDate", &FixedLocalVolSurface::maxDate,
            "Returns the maximum date.")
        .def("maxTime", &FixedLocalVolSurface::maxTime,
            "Returns the maximum time.")
        .def("minStrike", &FixedLocalVolSurface::minStrike,
            "Returns the minimum strike.")
        .def("maxStrike", &FixedLocalVolSurface::maxStrike,
            "Returns the maximum strike.");
}
