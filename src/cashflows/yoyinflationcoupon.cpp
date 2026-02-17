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
#include <ql/cashflows/yoyinflationcoupon.hpp>
#include <ql/indexes/inflationindex.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::yoyinflationcoupon(py::module_& m) {
    // YoYInflationCoupon
    py::class_<YoYInflationCoupon, InflationCoupon,
               ext::shared_ptr<YoYInflationCoupon>>(
        m, "YoYInflationCoupon",
        "Year-on-year inflation coupon.")
        .def(py::init<const Date&, Real,
                       const Date&, const Date&,
                       Natural,
                       const ext::shared_ptr<YoYInflationIndex>&,
                       const Period&,
                       CPI::InterpolationType,
                       const DayCounter&,
                       Real, Spread,
                       const Date&, const Date&>(),
            py::arg("paymentDate"),
            py::arg("nominal"),
            py::arg("startDate"),
            py::arg("endDate"),
            py::arg("fixingDays"),
            py::arg("index"),
            py::arg("observationLag"),
            py::arg("interpolation"),
            py::arg("dayCounter"),
            py::arg("gearing") = 1.0,
            py::arg("spread") = 0.0,
            py::arg("refPeriodStart") = Date(),
            py::arg("refPeriodEnd") = Date(),
            "Constructs a YoY inflation coupon.")
        .def("gearing", &YoYInflationCoupon::gearing,
            "Returns the gearing.")
        .def("spread", &YoYInflationCoupon::spread,
            "Returns the spread.")
        .def("adjustedFixing", &YoYInflationCoupon::adjustedFixing,
            "Returns the adjusted fixing.")
        .def("yoyIndex", &YoYInflationCoupon::yoyIndex,
            "Returns the YoY inflation index.")
        .def("interpolation", &YoYInflationCoupon::interpolation,
            "Returns the interpolation type.");

    // yoyInflationLeg builder
    py::class_<yoyInflationLeg>(m, "yoyInflationLeg",
        "Builder for year-on-year inflation legs.")
        .def(py::init<Schedule, Calendar,
                       ext::shared_ptr<YoYInflationIndex>,
                       const Period&,
                       CPI::InterpolationType>(),
            py::arg("schedule"),
            py::arg("calendar"),
            py::arg("index"),
            py::arg("observationLag"),
            py::arg("interpolation"),
            "Constructs a yoyInflationLeg builder.")
        .def("withNotionals",
            [](yoyInflationLeg& self, Real n) -> yoyInflationLeg& {
                return self.withNotionals(n);
            },
            py::return_value_policy::reference_internal, py::arg("nominal"))
        .def("withNotionals",
            [](yoyInflationLeg& self, const std::vector<Real>& n)
                -> yoyInflationLeg& {
                return self.withNotionals(n);
            },
            py::return_value_policy::reference_internal, py::arg("nominals"))
        .def("withPaymentDayCounter",
            [](yoyInflationLeg& self, const DayCounter& dc)
                -> yoyInflationLeg& {
                return self.withPaymentDayCounter(dc);
            },
            py::return_value_policy::reference_internal, py::arg("dayCounter"))
        .def("withPaymentAdjustment",
            [](yoyInflationLeg& self, BusinessDayConvention bdc)
                -> yoyInflationLeg& {
                return self.withPaymentAdjustment(bdc);
            },
            py::return_value_policy::reference_internal,
            py::arg("convention"))
        .def("withFixingDays",
            [](yoyInflationLeg& self, Natural days) -> yoyInflationLeg& {
                return self.withFixingDays(days);
            },
            py::return_value_policy::reference_internal,
            py::arg("fixingDays"))
        .def("withFixingDays",
            [](yoyInflationLeg& self, const std::vector<Natural>& days)
                -> yoyInflationLeg& {
                return self.withFixingDays(days);
            },
            py::return_value_policy::reference_internal,
            py::arg("fixingDays"))
        .def("withGearings",
            [](yoyInflationLeg& self, Real g) -> yoyInflationLeg& {
                return self.withGearings(g);
            },
            py::return_value_policy::reference_internal, py::arg("gearing"))
        .def("withGearings",
            [](yoyInflationLeg& self, const std::vector<Real>& g)
                -> yoyInflationLeg& {
                return self.withGearings(g);
            },
            py::return_value_policy::reference_internal, py::arg("gearings"))
        .def("withSpreads",
            [](yoyInflationLeg& self, Spread s) -> yoyInflationLeg& {
                return self.withSpreads(s);
            },
            py::return_value_policy::reference_internal, py::arg("spread"))
        .def("withSpreads",
            [](yoyInflationLeg& self, const std::vector<Spread>& s)
                -> yoyInflationLeg& {
                return self.withSpreads(s);
            },
            py::return_value_policy::reference_internal, py::arg("spreads"))
        .def("withCaps",
            [](yoyInflationLeg& self, Rate cap) -> yoyInflationLeg& {
                return self.withCaps(cap);
            },
            py::return_value_policy::reference_internal, py::arg("cap"))
        .def("withCaps",
            [](yoyInflationLeg& self, const std::vector<Rate>& caps)
                -> yoyInflationLeg& {
                return self.withCaps(caps);
            },
            py::return_value_policy::reference_internal, py::arg("caps"))
        .def("withFloors",
            [](yoyInflationLeg& self, Rate floor) -> yoyInflationLeg& {
                return self.withFloors(floor);
            },
            py::return_value_policy::reference_internal, py::arg("floor"))
        .def("withFloors",
            [](yoyInflationLeg& self, const std::vector<Rate>& floors)
                -> yoyInflationLeg& {
                return self.withFloors(floors);
            },
            py::return_value_policy::reference_internal, py::arg("floors"))
        .def("build",
            [](const yoyInflationLeg& self) {
                return static_cast<Leg>(self);
            },
            "Builds and returns the leg of cash flows.");
}
