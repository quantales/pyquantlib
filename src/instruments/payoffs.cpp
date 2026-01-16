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
}
