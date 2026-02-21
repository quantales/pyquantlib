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
#include <ql/instruments/nonstandardswap.hpp>
#include <ql/instruments/fixedvsfloatingswap.hpp>
#include <ql/indexes/iborindex.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::nonstandardswap(py::module_& m) {
    py::class_<NonstandardSwap, Swap, ext::shared_ptr<NonstandardSwap>>(
        m, "NonstandardSwap",
        "Nonstandard swap with period-dependent nominal and strike.")
        // Constructor from FixedVsFloatingSwap
        .def(py::init<const FixedVsFloatingSwap&>(),
            py::arg("fromVanilla"),
            "Constructs from a fixed-vs-floating swap.")
        // Scalar gearing/spread constructor
        .def(py::init([](Swap::Type type,
                         std::vector<Real> fixedNominal,
                         const std::vector<Real>& floatingNominal,
                         Schedule fixedSchedule,
                         std::vector<Real> fixedRate,
                         DayCounter fixedDayCount,
                         Schedule floatingSchedule,
                         ext::shared_ptr<IborIndex> iborIndex,
                         Real gearing,
                         Spread spread,
                         DayCounter floatingDayCount,
                         bool intermediateCapitalExchange,
                         bool finalCapitalExchange,
                         const py::object& paymentConvention) {
            ext::optional<BusinessDayConvention> pc = ext::nullopt;
            if (!paymentConvention.is_none())
                pc = paymentConvention.cast<BusinessDayConvention>();
            return ext::make_shared<NonstandardSwap>(
                type, std::move(fixedNominal), floatingNominal,
                std::move(fixedSchedule), std::move(fixedRate),
                std::move(fixedDayCount), std::move(floatingSchedule),
                std::move(iborIndex), gearing, spread,
                std::move(floatingDayCount),
                intermediateCapitalExchange, finalCapitalExchange, pc);
        }),
            py::arg("type"),
            py::arg("fixedNominal"),
            py::arg("floatingNominal"),
            py::arg("fixedSchedule"),
            py::arg("fixedRate"),
            py::arg("fixedDayCount"),
            py::arg("floatingSchedule"),
            py::arg("iborIndex"),
            py::arg("gearing"),
            py::arg("spread"),
            py::arg("floatingDayCount"),
            py::arg("intermediateCapitalExchange") = false,
            py::arg("finalCapitalExchange") = false,
            py::arg("paymentConvention") = py::none(),
            "Constructs with scalar gearing and spread.")
        // Vector gearings/spreads constructor
        .def(py::init([](Swap::Type type,
                         std::vector<Real> fixedNominal,
                         std::vector<Real> floatingNominal,
                         Schedule fixedSchedule,
                         std::vector<Real> fixedRate,
                         DayCounter fixedDayCount,
                         Schedule floatingSchedule,
                         ext::shared_ptr<IborIndex> iborIndex,
                         std::vector<Real> gearing,
                         std::vector<Spread> spread,
                         DayCounter floatingDayCount,
                         bool intermediateCapitalExchange,
                         bool finalCapitalExchange,
                         const py::object& paymentConvention) {
            ext::optional<BusinessDayConvention> pc = ext::nullopt;
            if (!paymentConvention.is_none())
                pc = paymentConvention.cast<BusinessDayConvention>();
            return ext::make_shared<NonstandardSwap>(
                type, std::move(fixedNominal), std::move(floatingNominal),
                std::move(fixedSchedule), std::move(fixedRate),
                std::move(fixedDayCount), std::move(floatingSchedule),
                std::move(iborIndex), std::move(gearing), std::move(spread),
                std::move(floatingDayCount),
                intermediateCapitalExchange, finalCapitalExchange, pc);
        }),
            py::arg("type"),
            py::arg("fixedNominal"),
            py::arg("floatingNominal"),
            py::arg("fixedSchedule"),
            py::arg("fixedRate"),
            py::arg("fixedDayCount"),
            py::arg("floatingSchedule"),
            py::arg("iborIndex"),
            py::arg("gearings"),
            py::arg("spreads"),
            py::arg("floatingDayCount"),
            py::arg("intermediateCapitalExchange") = false,
            py::arg("finalCapitalExchange") = false,
            py::arg("paymentConvention") = py::none(),
            "Constructs with vector gearings and spreads.")
        // Inspectors
        .def("type", &NonstandardSwap::type,
            "Returns the swap type.")
        .def("fixedNominal", &NonstandardSwap::fixedNominal,
            py::return_value_policy::reference_internal,
            "Returns the fixed leg nominals.")
        .def("floatingNominal", &NonstandardSwap::floatingNominal,
            py::return_value_policy::reference_internal,
            "Returns the floating leg nominals.")
        .def("fixedSchedule", &NonstandardSwap::fixedSchedule,
            py::return_value_policy::reference_internal,
            "Returns the fixed leg schedule.")
        .def("floatingSchedule", &NonstandardSwap::floatingSchedule,
            py::return_value_policy::reference_internal,
            "Returns the floating leg schedule.")
        .def("fixedRate", &NonstandardSwap::fixedRate,
            py::return_value_policy::reference_internal,
            "Returns the fixed rates.")
        .def("iborIndex", &NonstandardSwap::iborIndex,
            py::return_value_policy::reference_internal,
            "Returns the IBOR index.")
        .def("spread", &NonstandardSwap::spread,
            "Returns the scalar spread.")
        .def("gearing", &NonstandardSwap::gearing,
            "Returns the scalar gearing.")
        .def("spreads", &NonstandardSwap::spreads,
            py::return_value_policy::reference_internal,
            "Returns the spread vector.")
        .def("gearings", &NonstandardSwap::gearings,
            py::return_value_policy::reference_internal,
            "Returns the gearing vector.")
        .def("fixedDayCount", &NonstandardSwap::fixedDayCount,
            py::return_value_policy::reference_internal,
            "Returns the fixed leg day counter.")
        .def("floatingDayCount", &NonstandardSwap::floatingDayCount,
            py::return_value_policy::reference_internal,
            "Returns the floating leg day counter.")
        .def("paymentConvention", &NonstandardSwap::paymentConvention,
            "Returns the payment convention.")
        .def("fixedLeg", &NonstandardSwap::fixedLeg,
            py::return_value_policy::reference_internal,
            "Returns the fixed leg cash flows.")
        .def("floatingLeg", &NonstandardSwap::floatingLeg,
            py::return_value_policy::reference_internal,
            "Returns the floating leg cash flows.");
}
