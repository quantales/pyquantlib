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
#include <ql/cashflows/digitaliborcoupon.hpp>
#include <ql/cashflows/couponpricer.hpp>
#include <ql/cashflows/replication.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/position.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::digitaliborcoupon(py::module_& m) {
    // DigitalIborCoupon
    py::class_<DigitalIborCoupon, DigitalCoupon,
               ext::shared_ptr<DigitalIborCoupon>>(
        m, "DigitalIborCoupon",
        "Ibor coupon with digital call/put option.")
        .def(py::init([](const ext::shared_ptr<IborCoupon>& underlying,
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
            return ext::make_shared<DigitalIborCoupon>(
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
            "Constructs a digital Ibor coupon.");

    // DigitalIborLeg builder
    py::class_<DigitalIborLeg>(m, "DigitalIborLeg",
        "Helper class for building a leg of digital Ibor coupons.")
        .def(py::init<Schedule, ext::shared_ptr<IborIndex>>(),
            py::arg("schedule"), py::arg("index"),
            "Constructs from a schedule and Ibor index.")
        .def("withNotionals",
            [](DigitalIborLeg& self, Real n) -> DigitalIborLeg& {
                return self.withNotionals(n);
            },
            py::return_value_policy::reference_internal, py::arg("nominal"))
        .def("withNotionals",
            [](DigitalIborLeg& self, const std::vector<Real>& n) -> DigitalIborLeg& {
                return self.withNotionals(n);
            },
            py::return_value_policy::reference_internal, py::arg("nominals"))
        .def("withPaymentDayCounter",
            [](DigitalIborLeg& self, const DayCounter& dc) -> DigitalIborLeg& {
                return self.withPaymentDayCounter(dc);
            },
            py::return_value_policy::reference_internal, py::arg("dayCounter"))
        .def("withPaymentAdjustment",
            [](DigitalIborLeg& self, BusinessDayConvention bdc) -> DigitalIborLeg& {
                return self.withPaymentAdjustment(bdc);
            },
            py::return_value_policy::reference_internal, py::arg("convention"))
        .def("withFixingDays",
            [](DigitalIborLeg& self, Natural days) -> DigitalIborLeg& {
                return self.withFixingDays(days);
            },
            py::return_value_policy::reference_internal, py::arg("fixingDays"))
        .def("withFixingDays",
            [](DigitalIborLeg& self, const std::vector<Natural>& days) -> DigitalIborLeg& {
                return self.withFixingDays(days);
            },
            py::return_value_policy::reference_internal, py::arg("fixingDays"))
        .def("withGearings",
            [](DigitalIborLeg& self, Real g) -> DigitalIborLeg& {
                return self.withGearings(g);
            },
            py::return_value_policy::reference_internal, py::arg("gearing"))
        .def("withGearings",
            [](DigitalIborLeg& self, const std::vector<Real>& g) -> DigitalIborLeg& {
                return self.withGearings(g);
            },
            py::return_value_policy::reference_internal, py::arg("gearings"))
        .def("withSpreads",
            [](DigitalIborLeg& self, Spread s) -> DigitalIborLeg& {
                return self.withSpreads(s);
            },
            py::return_value_policy::reference_internal, py::arg("spread"))
        .def("withSpreads",
            [](DigitalIborLeg& self, const std::vector<Spread>& s) -> DigitalIborLeg& {
                return self.withSpreads(s);
            },
            py::return_value_policy::reference_internal, py::arg("spreads"))
        .def("inArrears",
            [](DigitalIborLeg& self, bool flag) -> DigitalIborLeg& {
                return self.inArrears(flag);
            },
            py::return_value_policy::reference_internal, py::arg("flag") = true)
        .def("withCallStrikes",
            [](DigitalIborLeg& self, Rate strike) -> DigitalIborLeg& {
                return self.withCallStrikes(strike);
            },
            py::return_value_policy::reference_internal, py::arg("strike"))
        .def("withCallStrikes",
            [](DigitalIborLeg& self, const std::vector<Rate>& strikes) -> DigitalIborLeg& {
                return self.withCallStrikes(strikes);
            },
            py::return_value_policy::reference_internal, py::arg("strikes"))
        .def("withLongCallOption",
            [](DigitalIborLeg& self, Position::Type type) -> DigitalIborLeg& {
                return self.withLongCallOption(type);
            },
            py::return_value_policy::reference_internal, py::arg("type"))
        .def("withCallATM",
            [](DigitalIborLeg& self, bool flag) -> DigitalIborLeg& {
                return self.withCallATM(flag);
            },
            py::return_value_policy::reference_internal, py::arg("flag") = true)
        .def("withCallPayoffs",
            [](DigitalIborLeg& self, Rate payoff) -> DigitalIborLeg& {
                return self.withCallPayoffs(payoff);
            },
            py::return_value_policy::reference_internal, py::arg("payoff"))
        .def("withCallPayoffs",
            [](DigitalIborLeg& self, const std::vector<Rate>& payoffs) -> DigitalIborLeg& {
                return self.withCallPayoffs(payoffs);
            },
            py::return_value_policy::reference_internal, py::arg("payoffs"))
        .def("withPutStrikes",
            [](DigitalIborLeg& self, Rate strike) -> DigitalIborLeg& {
                return self.withPutStrikes(strike);
            },
            py::return_value_policy::reference_internal, py::arg("strike"))
        .def("withPutStrikes",
            [](DigitalIborLeg& self, const std::vector<Rate>& strikes) -> DigitalIborLeg& {
                return self.withPutStrikes(strikes);
            },
            py::return_value_policy::reference_internal, py::arg("strikes"))
        .def("withLongPutOption",
            [](DigitalIborLeg& self, Position::Type type) -> DigitalIborLeg& {
                return self.withLongPutOption(type);
            },
            py::return_value_policy::reference_internal, py::arg("type"))
        .def("withPutATM",
            [](DigitalIborLeg& self, bool flag) -> DigitalIborLeg& {
                return self.withPutATM(flag);
            },
            py::return_value_policy::reference_internal, py::arg("flag") = true)
        .def("withPutPayoffs",
            [](DigitalIborLeg& self, Rate payoff) -> DigitalIborLeg& {
                return self.withPutPayoffs(payoff);
            },
            py::return_value_policy::reference_internal, py::arg("payoff"))
        .def("withPutPayoffs",
            [](DigitalIborLeg& self, const std::vector<Rate>& payoffs) -> DigitalIborLeg& {
                return self.withPutPayoffs(payoffs);
            },
            py::return_value_policy::reference_internal, py::arg("payoffs"))
        .def("withReplication",
            [](DigitalIborLeg& self,
               const ext::shared_ptr<DigitalReplication>& repl) -> DigitalIborLeg& {
                return self.withReplication(repl);
            },
            py::return_value_policy::reference_internal, py::arg("replication"))
        .def("withNakedOption",
            [](DigitalIborLeg& self, bool flag) -> DigitalIborLeg& {
                return self.withNakedOption(flag);
            },
            py::return_value_policy::reference_internal, py::arg("nakedOption") = true)
        .def("build",
            [](const DigitalIborLeg& self) {
                return static_cast<Leg>(self);
            },
            "Builds and returns the leg of cash flows.");
}
