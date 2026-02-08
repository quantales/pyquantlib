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
#include <ql/instruments/makevanillaswap.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::makevanillaswap(py::module_& m) {
    py::class_<MakeVanillaSwap>(m, "MakeVanillaSwap",
        "Helper class for constructing standard market swaps.")
        // Constructor with py::none() sentinel for Null<Rate>()
        .def(py::init([](const Period& swapTenor,
                         const ext::shared_ptr<IborIndex>& iborIndex,
                         const py::object& fixedRate,
                         const Period& forwardStart) {
            Rate r = fixedRate.is_none() ? Null<Rate>() : fixedRate.cast<Rate>();
            return MakeVanillaSwap(swapTenor, iborIndex, r, forwardStart);
        }),
            py::arg("swapTenor"),
            py::arg("iborIndex"),
            py::arg("fixedRate") = py::none(),
            py::arg("forwardStart") = Period(0, Days),
            "Constructs a vanilla swap builder.")
        // Builder methods
        .def("receiveFixed", &MakeVanillaSwap::receiveFixed,
            py::arg("flag") = true,
            py::return_value_policy::reference_internal,
            "Sets whether to receive fixed.")
        .def("withType", &MakeVanillaSwap::withType,
            py::arg("type"),
            py::return_value_policy::reference_internal,
            "Sets the swap type.")
        .def("withNominal", &MakeVanillaSwap::withNominal,
            py::arg("nominal"),
            py::return_value_policy::reference_internal,
            "Sets the nominal amount.")
        .def("withSettlementDays", &MakeVanillaSwap::withSettlementDays,
            py::arg("settlementDays"),
            py::return_value_policy::reference_internal,
            "Sets the settlement days.")
        .def("withEffectiveDate", &MakeVanillaSwap::withEffectiveDate,
            py::arg("date"),
            py::return_value_policy::reference_internal,
            "Sets the effective date.")
        .def("withTerminationDate", &MakeVanillaSwap::withTerminationDate,
            py::arg("date"),
            py::return_value_policy::reference_internal,
            "Sets the termination date.")
        .def("withRule", &MakeVanillaSwap::withRule,
            py::arg("rule"),
            py::return_value_policy::reference_internal,
            "Sets the date generation rule.")
        .def("withPaymentConvention", &MakeVanillaSwap::withPaymentConvention,
            py::arg("convention"),
            py::return_value_policy::reference_internal,
            "Sets the payment convention.")
        // Fixed leg methods
        .def("withFixedLegTenor", &MakeVanillaSwap::withFixedLegTenor,
            py::arg("tenor"),
            py::return_value_policy::reference_internal,
            "Sets the fixed leg tenor.")
        .def("withFixedLegCalendar", &MakeVanillaSwap::withFixedLegCalendar,
            py::arg("calendar"),
            py::return_value_policy::reference_internal,
            "Sets the fixed leg calendar.")
        .def("withFixedLegConvention", &MakeVanillaSwap::withFixedLegConvention,
            py::arg("convention"),
            py::return_value_policy::reference_internal,
            "Sets the fixed leg business day convention.")
        .def("withFixedLegTerminationDateConvention",
            &MakeVanillaSwap::withFixedLegTerminationDateConvention,
            py::arg("convention"),
            py::return_value_policy::reference_internal,
            "Sets the fixed leg termination date convention.")
        .def("withFixedLegRule", &MakeVanillaSwap::withFixedLegRule,
            py::arg("rule"),
            py::return_value_policy::reference_internal,
            "Sets the fixed leg date generation rule.")
        .def("withFixedLegEndOfMonth", &MakeVanillaSwap::withFixedLegEndOfMonth,
            py::arg("flag") = true,
            py::return_value_policy::reference_internal,
            "Sets the fixed leg end-of-month flag.")
        .def("withFixedLegFirstDate", &MakeVanillaSwap::withFixedLegFirstDate,
            py::arg("date"),
            py::return_value_policy::reference_internal,
            "Sets the fixed leg first date.")
        .def("withFixedLegNextToLastDate",
            &MakeVanillaSwap::withFixedLegNextToLastDate,
            py::arg("date"),
            py::return_value_policy::reference_internal,
            "Sets the fixed leg next-to-last date.")
        .def("withFixedLegDayCount", &MakeVanillaSwap::withFixedLegDayCount,
            py::arg("dayCount"),
            py::return_value_policy::reference_internal,
            "Sets the fixed leg day count convention.")
        // Floating leg methods
        .def("withFloatingLegTenor", &MakeVanillaSwap::withFloatingLegTenor,
            py::arg("tenor"),
            py::return_value_policy::reference_internal,
            "Sets the floating leg tenor.")
        .def("withFloatingLegCalendar", &MakeVanillaSwap::withFloatingLegCalendar,
            py::arg("calendar"),
            py::return_value_policy::reference_internal,
            "Sets the floating leg calendar.")
        .def("withFloatingLegConvention",
            &MakeVanillaSwap::withFloatingLegConvention,
            py::arg("convention"),
            py::return_value_policy::reference_internal,
            "Sets the floating leg business day convention.")
        .def("withFloatingLegTerminationDateConvention",
            &MakeVanillaSwap::withFloatingLegTerminationDateConvention,
            py::arg("convention"),
            py::return_value_policy::reference_internal,
            "Sets the floating leg termination date convention.")
        .def("withFloatingLegRule", &MakeVanillaSwap::withFloatingLegRule,
            py::arg("rule"),
            py::return_value_policy::reference_internal,
            "Sets the floating leg date generation rule.")
        .def("withFloatingLegEndOfMonth",
            &MakeVanillaSwap::withFloatingLegEndOfMonth,
            py::arg("flag") = true,
            py::return_value_policy::reference_internal,
            "Sets the floating leg end-of-month flag.")
        .def("withFloatingLegFirstDate",
            &MakeVanillaSwap::withFloatingLegFirstDate,
            py::arg("date"),
            py::return_value_policy::reference_internal,
            "Sets the floating leg first date.")
        .def("withFloatingLegNextToLastDate",
            &MakeVanillaSwap::withFloatingLegNextToLastDate,
            py::arg("date"),
            py::return_value_policy::reference_internal,
            "Sets the floating leg next-to-last date.")
        .def("withFloatingLegDayCount",
            &MakeVanillaSwap::withFloatingLegDayCount,
            py::arg("dayCount"),
            py::return_value_policy::reference_internal,
            "Sets the floating leg day count convention.")
        .def("withFloatingLegSpread", &MakeVanillaSwap::withFloatingLegSpread,
            py::arg("spread"),
            py::return_value_policy::reference_internal,
            "Sets the floating leg spread.")
        // Discounting term structure (hidden handle + explicit handle)
        .def("withDiscountingTermStructure",
            [](MakeVanillaSwap& self,
               const ext::shared_ptr<YieldTermStructure>& ts)
               -> MakeVanillaSwap& {
                return self.withDiscountingTermStructure(
                    Handle<YieldTermStructure>(ts));
            },
            py::arg("discountCurve"),
            py::return_value_policy::reference_internal,
            "Sets the discounting term structure.")
        .def("withDiscountingTermStructure",
            static_cast<MakeVanillaSwap& (MakeVanillaSwap::*)(
                const Handle<YieldTermStructure>&)>(
                &MakeVanillaSwap::withDiscountingTermStructure),
            py::arg("discountCurve"),
            py::return_value_policy::reference_internal,
            "Sets the discounting term structure (handle).")
        .def("withPricingEngine", &MakeVanillaSwap::withPricingEngine,
            py::arg("engine"),
            py::return_value_policy::reference_internal,
            "Sets the pricing engine.")
        .def("withIndexedCoupons", &MakeVanillaSwap::withIndexedCoupons,
            py::arg("flag") = true,
            py::return_value_policy::reference_internal,
            "Uses indexed coupons for the floating leg.")
        .def("withAtParCoupons", &MakeVanillaSwap::withAtParCoupons,
            py::arg("flag") = true,
            py::return_value_policy::reference_internal,
            "Uses at-par coupons for the floating leg.")
        // Conversion to VanillaSwap
        .def("swap", [](const MakeVanillaSwap& self) {
            return ext::shared_ptr<VanillaSwap>(self);
        }, "Builds and returns the VanillaSwap.");
}
