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
#include <ql/termstructures/globalbootstrap.hpp>
#include <ql/math/interpolations/linearinterpolation.hpp>
#include <ql/math/interpolations/loginterpolation.hpp>
#include <ql/math/interpolations/backwardflatinterpolation.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>

namespace py = pybind11;
using namespace QuantLib;

namespace {

template <typename Traits, typename Interpolator>
void bindGlobalBootstrapCurve(py::module_& m, const char* name, const char* doc) {
    using Curve = PiecewiseYieldCurve<Traits, Interpolator, GlobalBootstrap>;
    using Helpers = std::vector<ext::shared_ptr<RateHelper>>;
    using BootstrapHelpers = std::vector<ext::shared_ptr<BootstrapHelper<YieldTermStructure>>>;

    py::class_<Curve, YieldTermStructure, ext::shared_ptr<Curve>>(m, name, doc)
        // Reference date constructor with accuracy
        .def(py::init([](const Date& referenceDate,
                         const Helpers& instruments,
                         const DayCounter& dayCounter,
                         Real accuracy,
                         const std::vector<Real>& instrumentWeights) {
            return ext::make_shared<Curve>(
                referenceDate, instruments, dayCounter,
                Interpolator(),
                GlobalBootstrap<Curve>(accuracy, nullptr, nullptr,
                                       instrumentWeights));
        }),
             py::arg("referenceDate"),
             py::arg("instruments"),
             py::arg("dayCounter"),
             py::arg("accuracy") = Null<Real>(),
             py::arg("instrumentWeights") = std::vector<Real>(),
             "Constructs with global bootstrap using default optimizer.")
        // Reference date constructor with optimizer
        .def(py::init([](const Date& referenceDate,
                         const Helpers& instruments,
                         const DayCounter& dayCounter,
                         const ext::shared_ptr<OptimizationMethod>& optimizer,
                         const ext::shared_ptr<EndCriteria>& endCriteria,
                         const std::vector<Real>& instrumentWeights) {
            return ext::make_shared<Curve>(
                referenceDate, instruments, dayCounter,
                Interpolator(),
                GlobalBootstrap<Curve>(Null<Real>(), optimizer, endCriteria,
                                       instrumentWeights));
        }),
             py::arg("referenceDate"),
             py::arg("instruments"),
             py::arg("dayCounter"),
             py::arg("optimizer"),
             py::arg("endCriteria") = nullptr,
             py::arg("instrumentWeights") = std::vector<Real>(),
             "Constructs with global bootstrap using a custom optimizer.")
        // Reference date constructor with additional helpers and penalties
        .def(py::init([](const Date& referenceDate,
                         const Helpers& instruments,
                         const DayCounter& dayCounter,
                         const BootstrapHelpers& additionalHelpers,
                         const std::function<std::vector<Date>()>& additionalDates,
                         const std::function<Array()>& additionalPenalties,
                         Real accuracy,
                         const std::vector<Real>& instrumentWeights) {
            return ext::make_shared<Curve>(
                referenceDate, instruments, dayCounter,
                Interpolator(),
                GlobalBootstrap<Curve>(additionalHelpers, additionalDates,
                                       additionalPenalties, accuracy,
                                       nullptr, nullptr, nullptr,
                                       instrumentWeights));
        }),
             py::arg("referenceDate"),
             py::arg("instruments"),
             py::arg("dayCounter"),
             py::arg("additionalHelpers"),
             py::arg("additionalDates"),
             py::arg("additionalPenalties"),
             py::arg("accuracy") = Null<Real>(),
             py::arg("instrumentWeights") = std::vector<Real>(),
             "Constructs with global bootstrap, additional helpers, and penalty functions.")
        // Settlement days constructor with accuracy
        .def(py::init([](Natural settlementDays,
                         const Calendar& calendar,
                         const Helpers& instruments,
                         const DayCounter& dayCounter,
                         Real accuracy,
                         const std::vector<Real>& instrumentWeights) {
            return ext::make_shared<Curve>(
                settlementDays, calendar, instruments, dayCounter,
                Interpolator(),
                GlobalBootstrap<Curve>(accuracy, nullptr, nullptr,
                                       instrumentWeights));
        }),
             py::arg("settlementDays"),
             py::arg("calendar"),
             py::arg("instruments"),
             py::arg("dayCounter"),
             py::arg("accuracy") = Null<Real>(),
             py::arg("instrumentWeights") = std::vector<Real>(),
             "Constructs from settlement days with global bootstrap.")
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

void ql_termstructures::globalbootstrap(py::module_& m) {
    bindGlobalBootstrapCurve<Discount, LogLinear>(
        m, "PiecewiseLogLinearDiscountGlobal",
        "Piecewise yield curve using log-linear discount factor interpolation "
        "with global bootstrap.");

    bindGlobalBootstrapCurve<ZeroYield, Linear>(
        m, "PiecewiseLinearZeroGlobal",
        "Piecewise yield curve using linear zero-rate interpolation "
        "with global bootstrap.");

    bindGlobalBootstrapCurve<ForwardRate, BackwardFlat>(
        m, "PiecewiseBackwardFlatForwardGlobal",
        "Piecewise yield curve using backward-flat forward-rate interpolation "
        "with global bootstrap.");
}
