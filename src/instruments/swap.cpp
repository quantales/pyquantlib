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
#include <ql/instrument.hpp>
#include <ql/pricingengine.hpp>
#include <ql/instruments/swap.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::swap(py::module_& m) {
    // Swap::Type enum
    py::enum_<Swap::Type>(m, "SwapType",
        "Swap type: Payer or Receiver.")
        .value("Payer", Swap::Payer)
        .value("Receiver", Swap::Receiver);

    // Swap::arguments
    py::class_<Swap::arguments, PricingEngine::arguments,
        ext::shared_ptr<Swap::arguments>>(
        m, "SwapArguments",
        "Arguments for swap pricing.")
        .def(py::init<>())
        .def_readwrite("legs", &Swap::arguments::legs)
        .def_readwrite("payer", &Swap::arguments::payer)
        .def("validate", &Swap::arguments::validate);

    // Swap::results
    py::class_<Swap::results, Instrument::results,
        ext::shared_ptr<Swap::results>>(
        m, "SwapResults",
        "Results from swap pricing.")
        .def(py::init<>())
        .def_readwrite("legNPV", &Swap::results::legNPV)
        .def_readwrite("legBPS", &Swap::results::legBPS)
        .def_readwrite("startDiscounts", &Swap::results::startDiscounts)
        .def_readwrite("endDiscounts", &Swap::results::endDiscounts)
        .def_readwrite("npvDateDiscount", &Swap::results::npvDateDiscount)
        .def("reset", &Swap::results::reset);

    // Swap class
    py::class_<Swap, Instrument, ext::shared_ptr<Swap>>(
        m, "Swap",
        "Interest rate swap base class.")
        // Two-leg constructor
        .def(py::init<const Leg&, const Leg&>(),
            py::arg("firstLeg"), py::arg("secondLeg"),
            "Constructs swap from two legs. First leg is paid, second is received.")
        // Multi-leg constructor
        .def(py::init<const std::vector<Leg>&, const std::vector<bool>&>(),
            py::arg("legs"), py::arg("payer"),
            "Constructs multi-leg swap.")
        // Inspectors
        .def("isExpired", &Swap::isExpired,
            "Returns True if the swap has expired.")
        .def("numberOfLegs", &Swap::numberOfLegs,
            "Returns the number of legs.")
        .def("legs", &Swap::legs,
            py::return_value_policy::reference_internal,
            "Returns all legs.")
        .def("startDate", &Swap::startDate,
            "Returns the start date.")
        .def("maturityDate", &Swap::maturityDate,
            "Returns the maturity date.")
        .def("leg", &Swap::leg,
            py::return_value_policy::reference_internal,
            py::arg("j"),
            "Returns leg j.")
        .def("payer", &Swap::payer,
            py::arg("j"),
            "Returns True if leg j is paid.")
        // Results
        .def("legBPS", &Swap::legBPS,
            py::arg("j"),
            "Returns the BPS of leg j.")
        .def("legNPV", &Swap::legNPV,
            py::arg("j"),
            "Returns the NPV of leg j.")
        .def("startDiscounts", &Swap::startDiscounts,
            py::arg("j"),
            "Returns the start discount factor for leg j.")
        .def("endDiscounts", &Swap::endDiscounts,
            py::arg("j"),
            "Returns the end discount factor for leg j.")
        .def("npvDateDiscount", &Swap::npvDateDiscount,
            "Returns the discount factor at the NPV date.");
}
