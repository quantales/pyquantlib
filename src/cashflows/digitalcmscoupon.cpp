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
#include <ql/cashflows/digitalcmscoupon.hpp>
#include <ql/cashflows/couponpricer.hpp>
#include <ql/cashflows/replication.hpp>
#include <ql/indexes/swapindex.hpp>
#include <ql/position.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::digitalcmscoupon(py::module_& m) {
    // DigitalCmsCoupon
    py::class_<DigitalCmsCoupon, DigitalCoupon,
               ext::shared_ptr<DigitalCmsCoupon>>(
        m, "DigitalCmsCoupon",
        "CMS coupon with digital call/put option.")
        .def(py::init([](const ext::shared_ptr<CmsCoupon>& underlying,
                         const py::object& callStrike,
                         Position::Type callPosition,
                         bool isCallATMIncluded,
                         const py::object& callDigitalPayoff,
                         const py::object& putStrike,
                         Position::Type putPosition,
                         bool isPutATMIncluded,
                         const py::object& putDigitalPayoff,
                         const py::object& replication,
                         bool nakedOption) {
            Rate cs = callStrike.is_none() ? Null<Rate>() : callStrike.cast<Rate>();
            Rate cp = callDigitalPayoff.is_none() ? Null<Rate>() : callDigitalPayoff.cast<Rate>();
            Rate ps = putStrike.is_none() ? Null<Rate>() : putStrike.cast<Rate>();
            Rate pp = putDigitalPayoff.is_none() ? Null<Rate>() : putDigitalPayoff.cast<Rate>();
            ext::shared_ptr<DigitalReplication> repl;
            if (!replication.is_none())
                repl = replication.cast<ext::shared_ptr<DigitalReplication>>();
            return ext::make_shared<DigitalCmsCoupon>(
                underlying, cs, callPosition, isCallATMIncluded, cp,
                ps, putPosition, isPutATMIncluded, pp,
                repl, nakedOption);
        }),
            py::arg("underlying"),
            py::arg("callStrike") = py::none(),
            py::arg("callPosition") = Position::Long,
            py::arg("isCallATMIncluded") = false,
            py::arg("callDigitalPayoff") = py::none(),
            py::arg("putStrike") = py::none(),
            py::arg("putPosition") = Position::Long,
            py::arg("isPutATMIncluded") = false,
            py::arg("putDigitalPayoff") = py::none(),
            py::arg("replication") = py::none(),
            py::arg("nakedOption") = false,
            "Constructs a digital CMS coupon.");

    // DigitalCmsLeg builder
    py::class_<DigitalCmsLeg>(m, "DigitalCmsLeg",
        "Helper class for building a leg of digital CMS coupons.")
        .def(py::init<Schedule, ext::shared_ptr<SwapIndex>>(),
            py::arg("schedule"), py::arg("index"),
            "Constructs from a schedule and swap index.")
        .def("withNotionals",
            [](DigitalCmsLeg& self, Real n) -> DigitalCmsLeg& {
                return self.withNotionals(n);
            },
            py::return_value_policy::reference_internal, py::arg("nominal"))
        .def("withNotionals",
            [](DigitalCmsLeg& self, const std::vector<Real>& n) -> DigitalCmsLeg& {
                return self.withNotionals(n);
            },
            py::return_value_policy::reference_internal, py::arg("nominals"))
        .def("withPaymentDayCounter",
            [](DigitalCmsLeg& self, const DayCounter& dc) -> DigitalCmsLeg& {
                return self.withPaymentDayCounter(dc);
            },
            py::return_value_policy::reference_internal, py::arg("dayCounter"))
        .def("withPaymentAdjustment",
            [](DigitalCmsLeg& self, BusinessDayConvention bdc) -> DigitalCmsLeg& {
                return self.withPaymentAdjustment(bdc);
            },
            py::return_value_policy::reference_internal, py::arg("convention"))
        .def("withFixingDays",
            [](DigitalCmsLeg& self, Natural days) -> DigitalCmsLeg& {
                return self.withFixingDays(days);
            },
            py::return_value_policy::reference_internal, py::arg("fixingDays"))
        .def("withFixingDays",
            [](DigitalCmsLeg& self, const std::vector<Natural>& days) -> DigitalCmsLeg& {
                return self.withFixingDays(days);
            },
            py::return_value_policy::reference_internal, py::arg("fixingDays"))
        .def("withGearings",
            [](DigitalCmsLeg& self, Real g) -> DigitalCmsLeg& {
                return self.withGearings(g);
            },
            py::return_value_policy::reference_internal, py::arg("gearing"))
        .def("withGearings",
            [](DigitalCmsLeg& self, const std::vector<Real>& g) -> DigitalCmsLeg& {
                return self.withGearings(g);
            },
            py::return_value_policy::reference_internal, py::arg("gearings"))
        .def("withSpreads",
            [](DigitalCmsLeg& self, Spread s) -> DigitalCmsLeg& {
                return self.withSpreads(s);
            },
            py::return_value_policy::reference_internal, py::arg("spread"))
        .def("withSpreads",
            [](DigitalCmsLeg& self, const std::vector<Spread>& s) -> DigitalCmsLeg& {
                return self.withSpreads(s);
            },
            py::return_value_policy::reference_internal, py::arg("spreads"))
        .def("inArrears",
            [](DigitalCmsLeg& self, bool flag) -> DigitalCmsLeg& {
                return self.inArrears(flag);
            },
            py::return_value_policy::reference_internal, py::arg("flag") = true)
        .def("withCallStrikes",
            [](DigitalCmsLeg& self, Rate strike) -> DigitalCmsLeg& {
                return self.withCallStrikes(strike);
            },
            py::return_value_policy::reference_internal, py::arg("strike"))
        .def("withCallStrikes",
            [](DigitalCmsLeg& self, const std::vector<Rate>& strikes) -> DigitalCmsLeg& {
                return self.withCallStrikes(strikes);
            },
            py::return_value_policy::reference_internal, py::arg("strikes"))
        .def("withLongCallOption",
            [](DigitalCmsLeg& self, Position::Type type) -> DigitalCmsLeg& {
                return self.withLongCallOption(type);
            },
            py::return_value_policy::reference_internal, py::arg("type"))
        .def("withCallATM",
            [](DigitalCmsLeg& self, bool flag) -> DigitalCmsLeg& {
                return self.withCallATM(flag);
            },
            py::return_value_policy::reference_internal, py::arg("flag") = true)
        .def("withCallPayoffs",
            [](DigitalCmsLeg& self, Rate payoff) -> DigitalCmsLeg& {
                return self.withCallPayoffs(payoff);
            },
            py::return_value_policy::reference_internal, py::arg("payoff"))
        .def("withCallPayoffs",
            [](DigitalCmsLeg& self, const std::vector<Rate>& payoffs) -> DigitalCmsLeg& {
                return self.withCallPayoffs(payoffs);
            },
            py::return_value_policy::reference_internal, py::arg("payoffs"))
        .def("withPutStrikes",
            [](DigitalCmsLeg& self, Rate strike) -> DigitalCmsLeg& {
                return self.withPutStrikes(strike);
            },
            py::return_value_policy::reference_internal, py::arg("strike"))
        .def("withPutStrikes",
            [](DigitalCmsLeg& self, const std::vector<Rate>& strikes) -> DigitalCmsLeg& {
                return self.withPutStrikes(strikes);
            },
            py::return_value_policy::reference_internal, py::arg("strikes"))
        .def("withLongPutOption",
            [](DigitalCmsLeg& self, Position::Type type) -> DigitalCmsLeg& {
                return self.withLongPutOption(type);
            },
            py::return_value_policy::reference_internal, py::arg("type"))
        .def("withPutATM",
            [](DigitalCmsLeg& self, bool flag) -> DigitalCmsLeg& {
                return self.withPutATM(flag);
            },
            py::return_value_policy::reference_internal, py::arg("flag") = true)
        .def("withPutPayoffs",
            [](DigitalCmsLeg& self, Rate payoff) -> DigitalCmsLeg& {
                return self.withPutPayoffs(payoff);
            },
            py::return_value_policy::reference_internal, py::arg("payoff"))
        .def("withPutPayoffs",
            [](DigitalCmsLeg& self, const std::vector<Rate>& payoffs) -> DigitalCmsLeg& {
                return self.withPutPayoffs(payoffs);
            },
            py::return_value_policy::reference_internal, py::arg("payoffs"))
        .def("withReplication",
            [](DigitalCmsLeg& self,
               const ext::shared_ptr<DigitalReplication>& repl) -> DigitalCmsLeg& {
                return self.withReplication(repl);
            },
            py::return_value_policy::reference_internal, py::arg("replication"))
        .def("withNakedOption",
            [](DigitalCmsLeg& self, bool flag) -> DigitalCmsLeg& {
                return self.withNakedOption(flag);
            },
            py::return_value_policy::reference_internal, py::arg("nakedOption") = true)
        .def("build",
            [](const DigitalCmsLeg& self) {
                return static_cast<Leg>(self);
            },
            "Builds and returns the leg of cash flows.");
}
