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
#include <ql/instruments/makeois.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::makeois(py::module_& m) {
    py::class_<MakeOIS>(m, "MakeOIS",
        "Helper class for constructing overnight indexed swaps.")
        // Constructor with py::none() sentinel for Null<Rate>()
        .def(py::init([](const Period& swapTenor,
                         const ext::shared_ptr<OvernightIndex>& overnightIndex,
                         const py::object& fixedRate,
                         const Period& fwdStart) {
            Rate r = fixedRate.is_none() ? Null<Rate>() : fixedRate.cast<Rate>();
            return MakeOIS(swapTenor, overnightIndex, r, fwdStart);
        }),
            py::arg("swapTenor"),
            py::arg("overnightIndex"),
            py::arg("fixedRate") = py::none(),
            py::arg("fwdStart") = Period(0, Days),
            "Constructs an OIS builder.")
        // Builder methods
        .def("receiveFixed", &MakeOIS::receiveFixed,
            py::arg("flag") = true,
            py::return_value_policy::reference_internal,
            "Sets whether to receive fixed.")
        .def("withType", &MakeOIS::withType,
            py::arg("type"),
            py::return_value_policy::reference_internal,
            "Sets the swap type.")
        .def("withNominal", &MakeOIS::withNominal,
            py::arg("nominal"),
            py::return_value_policy::reference_internal,
            "Sets the nominal amount.")
        .def("withSettlementDays", &MakeOIS::withSettlementDays,
            py::arg("settlementDays"),
            py::return_value_policy::reference_internal,
            "Sets the settlement days.")
        .def("withEffectiveDate", &MakeOIS::withEffectiveDate,
            py::arg("date"),
            py::return_value_policy::reference_internal,
            "Sets the effective date.")
        .def("withTerminationDate", &MakeOIS::withTerminationDate,
            py::arg("date"),
            py::return_value_policy::reference_internal,
            "Sets the termination date.")
        .def("withRule", &MakeOIS::withRule,
            py::arg("rule"),
            py::return_value_policy::reference_internal,
            "Sets the date generation rule for both legs.")
        .def("withFixedLegRule", &MakeOIS::withFixedLegRule,
            py::arg("rule"),
            py::return_value_policy::reference_internal,
            "Sets the date generation rule for the fixed leg.")
        .def("withOvernightLegRule", &MakeOIS::withOvernightLegRule,
            py::arg("rule"),
            py::return_value_policy::reference_internal,
            "Sets the date generation rule for the overnight leg.")
        .def("withPaymentFrequency", &MakeOIS::withPaymentFrequency,
            py::arg("frequency"),
            py::return_value_policy::reference_internal,
            "Sets the payment frequency for both legs.")
        .def("withFixedLegPaymentFrequency",
            &MakeOIS::withFixedLegPaymentFrequency,
            py::arg("frequency"),
            py::return_value_policy::reference_internal,
            "Sets the payment frequency for the fixed leg.")
        .def("withOvernightLegPaymentFrequency",
            &MakeOIS::withOvernightLegPaymentFrequency,
            py::arg("frequency"),
            py::return_value_policy::reference_internal,
            "Sets the payment frequency for the overnight leg.")
        .def("withPaymentAdjustment", &MakeOIS::withPaymentAdjustment,
            py::arg("convention"),
            py::return_value_policy::reference_internal,
            "Sets the payment adjustment convention.")
        .def("withPaymentLag", &MakeOIS::withPaymentLag,
            py::arg("lag"),
            py::return_value_policy::reference_internal,
            "Sets the payment lag in days.")
        .def("withPaymentCalendar", &MakeOIS::withPaymentCalendar,
            py::arg("calendar"),
            py::return_value_policy::reference_internal,
            "Sets the payment calendar.")
        .def("withCalendar", &MakeOIS::withCalendar,
            py::arg("calendar"),
            py::return_value_policy::reference_internal,
            "Sets the calendar for both legs.")
        .def("withFixedLegCalendar", &MakeOIS::withFixedLegCalendar,
            py::arg("calendar"),
            py::return_value_policy::reference_internal,
            "Sets the calendar for the fixed leg.")
        .def("withOvernightLegCalendar", &MakeOIS::withOvernightLegCalendar,
            py::arg("calendar"),
            py::return_value_policy::reference_internal,
            "Sets the calendar for the overnight leg.")
        .def("withConvention", &MakeOIS::withConvention,
            py::arg("convention"),
            py::return_value_policy::reference_internal,
            "Sets the business day convention for both legs.")
        .def("withFixedLegConvention", &MakeOIS::withFixedLegConvention,
            py::arg("convention"),
            py::return_value_policy::reference_internal,
            "Sets the business day convention for the fixed leg.")
        .def("withOvernightLegConvention", &MakeOIS::withOvernightLegConvention,
            py::arg("convention"),
            py::return_value_policy::reference_internal,
            "Sets the business day convention for the overnight leg.")
        .def("withTerminationDateConvention",
            &MakeOIS::withTerminationDateConvention,
            py::arg("convention"),
            py::return_value_policy::reference_internal,
            "Sets the termination date convention for both legs.")
        .def("withFixedLegTerminationDateConvention",
            &MakeOIS::withFixedLegTerminationDateConvention,
            py::arg("convention"),
            py::return_value_policy::reference_internal,
            "Sets the termination date convention for the fixed leg.")
        .def("withOvernightLegTerminationDateConvention",
            &MakeOIS::withOvernightLegTerminationDateConvention,
            py::arg("convention"),
            py::return_value_policy::reference_internal,
            "Sets the termination date convention for the overnight leg.")
        .def("withEndOfMonth", &MakeOIS::withEndOfMonth,
            py::arg("flag") = true,
            py::return_value_policy::reference_internal,
            "Sets the end-of-month flag for both legs.")
        .def("withFixedLegEndOfMonth", &MakeOIS::withFixedLegEndOfMonth,
            py::arg("flag") = true,
            py::return_value_policy::reference_internal,
            "Sets the end-of-month flag for the fixed leg.")
        .def("withOvernightLegEndOfMonth",
            &MakeOIS::withOvernightLegEndOfMonth,
            py::arg("flag") = true,
            py::return_value_policy::reference_internal,
            "Sets the end-of-month flag for the overnight leg.")
        .def("withFixedLegDayCount", &MakeOIS::withFixedLegDayCount,
            py::arg("dayCount"),
            py::return_value_policy::reference_internal,
            "Sets the day count convention for the fixed leg.")
        .def("withOvernightLegSpread", &MakeOIS::withOvernightLegSpread,
            py::arg("spread"),
            py::return_value_policy::reference_internal,
            "Sets the spread on the overnight leg.")
        // Hidden handle constructor for discounting term structure
        .def("withDiscountingTermStructure",
            [](MakeOIS& self,
               const ext::shared_ptr<YieldTermStructure>& ts) -> MakeOIS& {
                return self.withDiscountingTermStructure(
                    Handle<YieldTermStructure>(ts));
            },
            py::arg("discountCurve"),
            py::return_value_policy::reference_internal,
            "Sets the discounting term structure.")
        // Explicit handle overload
        .def("withDiscountingTermStructure",
            static_cast<MakeOIS& (MakeOIS::*)(
                const Handle<YieldTermStructure>&)>(
                &MakeOIS::withDiscountingTermStructure),
            py::arg("discountCurve"),
            py::return_value_policy::reference_internal,
            "Sets the discounting term structure (handle).")
        .def("withTelescopicValueDates", &MakeOIS::withTelescopicValueDates,
            py::arg("flag"),
            py::return_value_policy::reference_internal,
            "Enables telescopic value dates.")
        .def("withAveragingMethod", &MakeOIS::withAveragingMethod,
            py::arg("averagingMethod"),
            py::return_value_policy::reference_internal,
            "Sets the rate averaging method.")
        .def("withLookbackDays", &MakeOIS::withLookbackDays,
            py::arg("lookbackDays"),
            py::return_value_policy::reference_internal,
            "Sets the lookback days.")
        .def("withLockoutDays", &MakeOIS::withLockoutDays,
            py::arg("lockoutDays"),
            py::return_value_policy::reference_internal,
            "Sets the lockout days.")
        .def("withObservationShift", &MakeOIS::withObservationShift,
            py::arg("flag") = true,
            py::return_value_policy::reference_internal,
            "Enables observation shift.")
        .def("withPricingEngine", &MakeOIS::withPricingEngine,
            py::arg("engine"),
            py::return_value_policy::reference_internal,
            "Sets the pricing engine.")
        // Conversion to OvernightIndexedSwap
        .def("ois", [](const MakeOIS& self) {
            return ext::shared_ptr<OvernightIndexedSwap>(self);
        }, "Builds and returns the OvernightIndexedSwap.");
}
