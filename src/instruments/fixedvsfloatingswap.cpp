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
#include <ql/instruments/swap.hpp>
#include <ql/instruments/fixedvsfloatingswap.hpp>
#include <ql/indexes/iborindex.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::fixedvsfloatingswap(py::module_& m) {
    // FixedVsFloatingSwap::arguments
    py::class_<FixedVsFloatingSwap::arguments, Swap::arguments,
        ext::shared_ptr<FixedVsFloatingSwap::arguments>>(
        m, "FixedVsFloatingSwapArguments",
        "Arguments for fixed vs floating swap pricing.")
        .def(py::init<>())
        .def_readwrite("type", &FixedVsFloatingSwap::arguments::type)
        .def_readwrite("nominal", &FixedVsFloatingSwap::arguments::nominal)
        .def_readwrite("fixedNominals", &FixedVsFloatingSwap::arguments::fixedNominals)
        .def_readwrite("fixedResetDates", &FixedVsFloatingSwap::arguments::fixedResetDates)
        .def_readwrite("fixedPayDates", &FixedVsFloatingSwap::arguments::fixedPayDates)
        .def_readwrite("floatingNominals", &FixedVsFloatingSwap::arguments::floatingNominals)
        .def_readwrite("floatingAccrualTimes", &FixedVsFloatingSwap::arguments::floatingAccrualTimes)
        .def_readwrite("floatingResetDates", &FixedVsFloatingSwap::arguments::floatingResetDates)
        .def_readwrite("floatingFixingDates", &FixedVsFloatingSwap::arguments::floatingFixingDates)
        .def_readwrite("floatingPayDates", &FixedVsFloatingSwap::arguments::floatingPayDates)
        .def_readwrite("fixedCoupons", &FixedVsFloatingSwap::arguments::fixedCoupons)
        .def_readwrite("floatingSpreads", &FixedVsFloatingSwap::arguments::floatingSpreads)
        .def_readwrite("floatingCoupons", &FixedVsFloatingSwap::arguments::floatingCoupons);

    // FixedVsFloatingSwap::results
    py::class_<FixedVsFloatingSwap::results, Swap::results,
        ext::shared_ptr<FixedVsFloatingSwap::results>>(
        m, "FixedVsFloatingSwapResults",
        "Results from fixed vs floating swap pricing.")
        .def(py::init<>())
        .def_readwrite("fairRate", &FixedVsFloatingSwap::results::fairRate)
        .def_readwrite("fairSpread", &FixedVsFloatingSwap::results::fairSpread);

    // FixedVsFloatingSwap class
    py::class_<FixedVsFloatingSwap, Swap, ext::shared_ptr<FixedVsFloatingSwap>>(
        m, "FixedVsFloatingSwap",
        "Fixed vs floating swap base class.")
        // Inspectors
        .def("type", &FixedVsFloatingSwap::type,
            "Returns the swap type (Payer or Receiver).")
        .def("nominal", &FixedVsFloatingSwap::nominal,
            "Returns the nominal (throws if not constant).")
        .def("nominals", &FixedVsFloatingSwap::nominals,
            py::return_value_policy::reference_internal,
            "Returns the nominals (throws if different for legs).")
        .def("fixedNominals", &FixedVsFloatingSwap::fixedNominals,
            py::return_value_policy::reference_internal,
            "Returns the fixed leg nominals.")
        .def("fixedSchedule", &FixedVsFloatingSwap::fixedSchedule,
            py::return_value_policy::reference_internal,
            "Returns the fixed leg schedule.")
        .def("fixedRate", &FixedVsFloatingSwap::fixedRate,
            "Returns the fixed rate.")
        .def("fixedDayCount", &FixedVsFloatingSwap::fixedDayCount,
            py::return_value_policy::reference_internal,
            "Returns the fixed leg day counter.")
        .def("floatingNominals", &FixedVsFloatingSwap::floatingNominals,
            py::return_value_policy::reference_internal,
            "Returns the floating leg nominals.")
        .def("floatingSchedule", &FixedVsFloatingSwap::floatingSchedule,
            py::return_value_policy::reference_internal,
            "Returns the floating leg schedule.")
        .def("iborIndex", &FixedVsFloatingSwap::iborIndex,
            "Returns the IBOR index.")
        .def("spread", &FixedVsFloatingSwap::spread,
            "Returns the floating leg spread.")
        .def("floatingDayCount", &FixedVsFloatingSwap::floatingDayCount,
            py::return_value_policy::reference_internal,
            "Returns the floating leg day counter.")
        .def("paymentConvention", &FixedVsFloatingSwap::paymentConvention,
            "Returns the payment business day convention.")
        .def("fixedLeg", &FixedVsFloatingSwap::fixedLeg,
            py::return_value_policy::reference_internal,
            "Returns the fixed leg cash flows.")
        .def("floatingLeg", &FixedVsFloatingSwap::floatingLeg,
            py::return_value_policy::reference_internal,
            "Returns the floating leg cash flows.")
        // Results
        .def("fixedLegBPS", &FixedVsFloatingSwap::fixedLegBPS,
            "Returns the BPS of the fixed leg.")
        .def("fixedLegNPV", &FixedVsFloatingSwap::fixedLegNPV,
            "Returns the NPV of the fixed leg.")
        .def("fairRate", &FixedVsFloatingSwap::fairRate,
            "Returns the fair fixed rate.")
        .def("floatingLegBPS", &FixedVsFloatingSwap::floatingLegBPS,
            "Returns the BPS of the floating leg.")
        .def("floatingLegNPV", &FixedVsFloatingSwap::floatingLegNPV,
            "Returns the NPV of the floating leg.")
        .def("fairSpread", &FixedVsFloatingSwap::fairSpread,
            "Returns the fair spread.");
}
