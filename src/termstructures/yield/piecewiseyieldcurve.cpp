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
#include <ql/termstructures/yield/piecewiseyieldcurve.hpp>
#include <ql/termstructures/yield/ratehelpers.hpp>
#include <ql/termstructures/yield/bootstraptraits.hpp>
#include <ql/math/interpolations/linearinterpolation.hpp>
#include <ql/math/interpolations/loginterpolation.hpp>
#include <ql/math/interpolations/backwardflatinterpolation.hpp>
#include <ql/math/interpolations/cubicinterpolation.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

namespace {

template <typename Traits, typename Interpolator>
void bindPiecewiseCurve(py::module_& m, const char* name, const char* doc) {
    using Curve = PiecewiseYieldCurve<Traits, Interpolator>;
    using Helpers = std::vector<ext::shared_ptr<RateHelper>>;

    py::class_<Curve, YieldTermStructure, ext::shared_ptr<Curve>>(m, name, doc)
        // Reference date constructor
        .def(py::init([](const Date& referenceDate,
                         const Helpers& instruments,
                         const DayCounter& dayCounter) {
            return ext::make_shared<Curve>(referenceDate, instruments, dayCounter);
        }),
             py::arg("referenceDate"),
             py::arg("instruments"),
             py::arg("dayCounter"),
             "Constructs from reference date, instruments, and day counter.")
        // Settlement days constructor
        .def(py::init([](Natural settlementDays,
                         const Calendar& calendar,
                         const Helpers& instruments,
                         const DayCounter& dayCounter) {
            return ext::make_shared<Curve>(
                settlementDays, calendar, instruments, dayCounter);
        }),
             py::arg("settlementDays"),
             py::arg("calendar"),
             py::arg("instruments"),
             py::arg("dayCounter"),
             "Constructs from settlement days, calendar, instruments, and day counter.")
        .def("times", &Curve::times,
             py::return_value_policy::copy,
             "Returns the interpolation times.")
        .def("dates", &Curve::dates,
             py::return_value_policy::copy,
             "Returns the interpolation dates.")
        .def("data", &Curve::data,
             py::return_value_policy::copy,
             "Returns the interpolated data values.")
        .def("nodes", &Curve::nodes,
             "Returns (date, value) pairs for all nodes.");
}

}  // anonymous namespace

void ql_termstructures::piecewiseyieldcurve(py::module_& m) {
    bindPiecewiseCurve<Discount, LogLinear>(
        m, "PiecewiseLogLinearDiscount",
        "Piecewise yield curve using log-linear discount factor interpolation.");

    bindPiecewiseCurve<Discount, Linear>(
        m, "PiecewiseLinearDiscount",
        "Piecewise yield curve using linear discount factor interpolation.");

    bindPiecewiseCurve<ZeroYield, Linear>(
        m, "PiecewiseLinearZero",
        "Piecewise yield curve using linear zero-rate interpolation.");

    bindPiecewiseCurve<ZeroYield, Cubic>(
        m, "PiecewiseCubicZero",
        "Piecewise yield curve using cubic zero-rate interpolation.");

    bindPiecewiseCurve<ForwardRate, BackwardFlat>(
        m, "PiecewiseFlatForward",
        "Piecewise yield curve using backward-flat forward-rate interpolation.");
}
