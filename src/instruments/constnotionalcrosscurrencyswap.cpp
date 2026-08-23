/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2026 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/currency.hpp>
#include <ql/instruments/constnotionalcrosscurrencyswap.hpp>
#include <ql/instruments/swap.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::constnotionalcrosscurrencyswap(py::module_& m) {
    py::class_<ConstNotionalCrossCurrencySwap::arguments, Swap::arguments,
               ext::shared_ptr<ConstNotionalCrossCurrencySwap::arguments>>(
        m, "ConstNotionalCrossCurrencySwapArguments",
        "Arguments for cross-currency swap pricing.")
        .def(py::init<>())
        .def_readwrite("currencies",
            &ConstNotionalCrossCurrencySwap::arguments::currencies)
        .def("validate", &ConstNotionalCrossCurrencySwap::arguments::validate);

    py::class_<ConstNotionalCrossCurrencySwap::results, Swap::results,
               ext::shared_ptr<ConstNotionalCrossCurrencySwap::results>>(
        m, "ConstNotionalCrossCurrencySwapResults",
        "Results from cross-currency swap pricing.")
        .def(py::init<>())
        .def_readwrite("inCcyLegNPV",
            &ConstNotionalCrossCurrencySwap::results::inCcyLegNPV)
        .def_readwrite("inCcyLegBPS",
            &ConstNotionalCrossCurrencySwap::results::inCcyLegBPS)
        .def_readwrite("npvDateDiscounts",
            &ConstNotionalCrossCurrencySwap::results::npvDateDiscounts)
        .def("reset", &ConstNotionalCrossCurrencySwap::results::reset);

    py::class_<ConstNotionalCrossCurrencySwap, Swap,
               ext::shared_ptr<ConstNotionalCrossCurrencySwap>>(
        m, "ConstNotionalCrossCurrencySwap",
        "Cross-currency swap with constant notionals exchanged at inception "
        "and maturity.")
        .def(py::init<const Leg&, const Currency&, const Leg&, const Currency&>(),
            py::arg("firstLeg"), py::arg("firstLegCurrency"),
            py::arg("secondLeg"), py::arg("secondLegCurrency"),
            "Constructs from two legs. The first leg is paid, the second received.")
        .def(py::init<const std::vector<Leg>&, const std::vector<bool>&,
                      const std::vector<Currency>&>(),
            py::arg("legs"), py::arg("payer"), py::arg("currencies"),
            "Constructs a multi-leg swap with one currency per leg.")
        .def("legCurrency", &ConstNotionalCrossCurrencySwap::legCurrency,
            py::arg("j"),
            "Returns the currency of leg j.")
        .def("inCcyLegBPS", &ConstNotionalCrossCurrencySwap::inCcyLegBPS,
            py::arg("j"),
            "Returns the BPS of leg j in its own currency.")
        .def("inCcyLegNPV", &ConstNotionalCrossCurrencySwap::inCcyLegNPV,
            py::arg("j"),
            "Returns the NPV of leg j in its own currency.")
        .def("npvDateDiscounts",
            &ConstNotionalCrossCurrencySwap::npvDateDiscounts,
            py::arg("j"),
            "Returns the NPV-date discount factor applied to leg j.");
}
