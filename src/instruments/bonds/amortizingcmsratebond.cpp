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
#include <ql/instruments/bonds/amortizingcmsratebond.hpp>
#include <ql/indexes/swapindex.hpp>
#include <ql/time/daycounter.hpp>
#include <ql/time/schedule.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::amortizingcmsratebond(py::module_& m) {
    py::class_<AmortizingCmsRateBond, Bond, ext::shared_ptr<AmortizingCmsRateBond>>(
        m, "AmortizingCmsRateBond",
        "Amortizing CMS-rate bond.")
        .def(py::init([](Natural settlementDays,
                         const std::vector<Real>& notionals,
                         Schedule schedule,
                         const ext::shared_ptr<SwapIndex>& index,
                         const DayCounter& paymentDayCounter,
                         BusinessDayConvention paymentConvention,
                         const py::object& fixingDays,
                         const std::vector<Real>& gearings,
                         const std::vector<Spread>& spreads,
                         const std::vector<Rate>& caps,
                         const std::vector<Rate>& floors,
                         bool inArrears,
                         const Date& issueDate,
                         const std::vector<Real>& redemptions) {
            Natural fd = Null<Natural>();
            if (!fixingDays.is_none())
                fd = fixingDays.cast<Natural>();
            return ext::make_shared<AmortizingCmsRateBond>(
                settlementDays, notionals, std::move(schedule), index,
                paymentDayCounter, paymentConvention, fd,
                gearings, spreads, caps, floors,
                inArrears, issueDate, redemptions);
        }),
            py::arg("settlementDays"),
            py::arg("notionals"),
            py::arg("schedule"),
            py::arg("index"),
            py::arg("paymentDayCounter"),
            py::arg("paymentConvention") = Following,
            py::arg("fixingDays") = py::none(),
            py::arg("gearings") = std::vector<Real>{1.0},
            py::arg("spreads") = std::vector<Spread>{0.0},
            py::arg("caps") = std::vector<Rate>{},
            py::arg("floors") = std::vector<Rate>{},
            py::arg("inArrears") = false,
            py::arg("issueDate") = Date(),
            py::arg("redemptions") = std::vector<Real>{100.0},
            "Constructs an amortizing CMS-rate bond.");
}
