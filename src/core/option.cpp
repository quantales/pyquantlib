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
#include <ql/option.hpp>
#include <ql/payoff.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_core::option(py::module_& m) {
    py::module_ base = m.def_submodule("base", "Abstract base classes");

    py::enum_<Option::Type>(m, "OptionType", "Option type (call or put).")
        .value("Call", Option::Call, "Call option.")
        .value("Put", Option::Put, "Put option.")
        .export_values();

    auto pyOption = py::class_<Option, PyOption, ext::shared_ptr<Option>, Instrument>(
        base, "Option", "Abstract base class for options.")
        .def(py::init<ext::shared_ptr<Payoff>, ext::shared_ptr<Exercise>>(),
            py::arg("payoff"), py::arg("exercise"),
            "Constructs with payoff and exercise.")
        .def("payoff", &Option::payoff,
            "Returns the option payoff.")
        .def("exercise", &Option::exercise,
            "Returns the exercise style.");

    py::class_<Option::arguments, PricingEngine::arguments,
        ext::shared_ptr<Option::arguments>>(pyOption, "arguments",
        "Arguments for option pricing engines.")
        .def(py::init<>())
        .def_readwrite("payoff", &Option::arguments::payoff,
            "The option payoff.")
        .def_readwrite("exercise", &Option::arguments::exercise,
            "The exercise style.");

    py::class_<Greeks, ext::shared_ptr<Greeks>>(m, "Greeks",
        "Container for first-order Greeks.")
        .def(py::init<>())
        .def_readwrite("delta", &Greeks::delta, "Delta sensitivity.")
        .def_readwrite("gamma", &Greeks::gamma, "Gamma sensitivity.")
        .def_readwrite("theta", &Greeks::theta, "Theta sensitivity.")
        .def_readwrite("vega", &Greeks::vega, "Vega sensitivity.")
        .def_readwrite("rho", &Greeks::rho, "Rho sensitivity.")
        .def_readwrite("dividendRho", &Greeks::dividendRho, "Dividend rho sensitivity.");

    py::class_<MoreGreeks, ext::shared_ptr<MoreGreeks>>(m, "MoreGreeks",
        "Container for additional Greeks.")
        .def(py::init<>())
        .def_readwrite("itmCashProbability", &MoreGreeks::itmCashProbability,
            "ITM cash probability.")
        .def_readwrite("strikeSensitivity", &MoreGreeks::strikeSensitivity,
            "Strike sensitivity.");
}
