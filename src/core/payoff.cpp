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
#include <ql/payoff.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_core::payoff(py::module_& m) {
    py::module_ base = m.def_submodule("base", "Abstract base classes");

    py::class_<Payoff, PyPayoff, ext::shared_ptr<Payoff>>(base, "Payoff",
        "Abstract base class for option payoffs.")
        .def(py::init_alias<>())
        .def("name", &Payoff::name,
            "Returns the payoff name.")
        .def("description", &Payoff::description,
            "Returns the payoff description.")
        .def("__call__", [](const Payoff& payoff, Real price) {
                return payoff(price);
            },
            py::arg("price"),
            "Calculates the payoff for a given price.");
}
