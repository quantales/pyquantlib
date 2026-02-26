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
#include "pyquantlib/trampolines.h"
#include <ql/instruments/payoffs.hpp>
#include <ql/option.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::strikedtypepayoff(py::module_& m) {
    py::module_ base = m.def_submodule("base", "Abstract base classes");

    // StrikedTypePayoff ABC - no py::init since constructor is protected
    py::class_<StrikedTypePayoff, PyStrikedTypePayoff,
               ext::shared_ptr<StrikedTypePayoff>, Payoff>(
        base, "StrikedTypePayoff",
        "Abstract base class for payoffs with strike and option type.")
        .def("optionType", &StrikedTypePayoff::optionType,
            "Returns the option type (Call or Put).")
        .def("strike", &StrikedTypePayoff::strike,
            "Returns the strike price.");
}

void ql_instruments::payoffs(py::module_& m) {
    py::class_<PlainVanillaPayoff, StrikedTypePayoff,
               ext::shared_ptr<PlainVanillaPayoff>>(
        m, "PlainVanillaPayoff",
        "Plain vanilla payoff (max(S-K,0) for call, max(K-S,0) for put).")
        .def(py::init<Option::Type, Real>(),
             py::arg("type"), py::arg("strike"));

    py::class_<CashOrNothingPayoff, StrikedTypePayoff,
               ext::shared_ptr<CashOrNothingPayoff>>(
        m, "CashOrNothingPayoff",
        "Binary payoff: fixed cash amount if in the money, zero otherwise.")
        .def(py::init<Option::Type, Real, Real>(),
             py::arg("type"), py::arg("strike"), py::arg("cashPayoff"))
        .def("cashPayoff", &CashOrNothingPayoff::cashPayoff,
            "Returns the cash payoff amount.");

    py::class_<AssetOrNothingPayoff, StrikedTypePayoff,
               ext::shared_ptr<AssetOrNothingPayoff>>(
        m, "AssetOrNothingPayoff",
        "Binary payoff: asset value if in the money, zero otherwise.")
        .def(py::init<Option::Type, Real>(),
             py::arg("type"), py::arg("strike"));

    py::class_<GapPayoff, StrikedTypePayoff,
               ext::shared_ptr<GapPayoff>>(
        m, "GapPayoff",
        "Gap payoff: vanilla minus digital, with two strikes.")
        .def(py::init<Option::Type, Real, Real>(),
             py::arg("type"), py::arg("strike"), py::arg("secondStrike"))
        .def("secondStrike", &GapPayoff::secondStrike,
            "Returns the second (payoff) strike.");

    py::class_<PercentageStrikePayoff, StrikedTypePayoff,
               ext::shared_ptr<PercentageStrikePayoff>>(
        m, "PercentageStrikePayoff",
        "Payoff with strike expressed as moneyness percentage.")
        .def(py::init<Option::Type, Real>(),
             py::arg("type"), py::arg("moneyness"));

    py::class_<SuperFundPayoff, StrikedTypePayoff,
               ext::shared_ptr<SuperFundPayoff>>(
        m, "SuperFundPayoff",
        "Binary superfund payoff between two strikes (normalized by lower strike).")
        .def(py::init<Real, Real>(),
             py::arg("strike"), py::arg("secondStrike"))
        .def("secondStrike", &SuperFundPayoff::secondStrike,
            "Returns the second strike.");

    py::class_<SuperSharePayoff, StrikedTypePayoff,
               ext::shared_ptr<SuperSharePayoff>>(
        m, "SuperSharePayoff",
        "Binary supershare payoff: fixed cash between two strikes.")
        .def(py::init<Real, Real, Real>(),
             py::arg("strike"), py::arg("secondStrike"), py::arg("cashPayoff"))
        .def("secondStrike", &SuperSharePayoff::secondStrike,
            "Returns the second strike.")
        .def("cashPayoff", &SuperSharePayoff::cashPayoff,
            "Returns the cash payoff amount.");

    py::class_<FloatingTypePayoff, Payoff,
               ext::shared_ptr<FloatingTypePayoff>>(
        m, "FloatingTypePayoff",
        "Floating-strike payoff (for lookback options).")
        .def(py::init<Option::Type>(),
             py::arg("type"));
}
