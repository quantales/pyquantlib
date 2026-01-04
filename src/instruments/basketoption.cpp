/*
 * PyQuantLib: Python bindings for QuantLib
 * Copyright (c) 2025 Yassine Idyiahia
 *
 * QuantLib is Copyright (c) 2000-2025 The QuantLib Authors
 * QuantLib is free software under a modified BSD license.
 * See http://quantlib.org/ for more information.
 *
 * Source: https://github.com/quantales/pyquantlib
 * Licensed under the BSD 3-Clause License. See LICENSE file for details.
 */

#include "pyquantlib/pyquantlib.h"
#include "pyquantlib/trampolines.h"
#include <ql/instruments/basketoption.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::basketoption(py::module_& m) {
    py::module_ base = m.def_submodule("base", "Abstract base classes");

    // BasketPayoff ABC
    py::class_<BasketPayoff, PyBasketPayoff, ext::shared_ptr<BasketPayoff>, Payoff>(
        base, "BasketPayoff", "Abstract base class for basket payoffs.")
        .def(py::init<ext::shared_ptr<Payoff>>(),
            py::arg("basePayoff"),
            "Constructs with base payoff.")
        .def("name", &BasketPayoff::name,
            "Returns the payoff name.")
        .def("description", &BasketPayoff::description,
            "Returns the payoff description.")
        .def("__call__", [](const BasketPayoff& p, Real price) {
                return p(price);
            },
            py::arg("price"),
            "Calculates payoff for a single price.")
        .def("__call__", [](const BasketPayoff& p, const Array& a) {
                return p(a);
            },
            py::arg("prices"),
            "Calculates payoff for an array of prices.")
        .def("__call__", [](const BasketPayoff& p, const std::vector<Real>& v) {
                return p(Array(v.begin(), v.end()));
            },
            py::arg("prices"),
            "Calculates payoff for a list of prices.")
        .def("accumulate", &BasketPayoff::accumulate,
            py::arg("prices"),
            "Accumulates prices into a single value.")
        .def("accumulate", [](const BasketPayoff& p, const std::vector<Real>& v) {
                return p.accumulate(Array(v.begin(), v.end()));
            },
            py::arg("prices"),
            "Accumulates a list of prices into a single value.")
        .def("basePayoff", &BasketPayoff::basePayoff,
            "Returns the underlying payoff.");

    // MinBasketPayoff
    py::class_<MinBasketPayoff, ext::shared_ptr<MinBasketPayoff>, BasketPayoff>(
        m, "MinBasketPayoff", "Payoff based on minimum of basket prices.")
        .def(py::init<ext::shared_ptr<Payoff>>(),
            py::arg("basePayoff"),
            "Constructs with base payoff.");

    // MaxBasketPayoff
    py::class_<MaxBasketPayoff, ext::shared_ptr<MaxBasketPayoff>, BasketPayoff>(
        m, "MaxBasketPayoff", "Payoff based on maximum of basket prices.")
        .def(py::init<ext::shared_ptr<Payoff>>(),
            py::arg("basePayoff"),
            "Constructs with base payoff.");

    // AverageBasketPayoff
    py::class_<AverageBasketPayoff, ext::shared_ptr<AverageBasketPayoff>, BasketPayoff>(
        m, "AverageBasketPayoff", "Payoff based on weighted average of basket prices.")
        .def(py::init<ext::shared_ptr<Payoff>, Array>(),
            py::arg("basePayoff"), py::arg("weights"),
            "Constructs with base payoff and weights.")
        .def(py::init<ext::shared_ptr<Payoff>, Size>(),
            py::arg("basePayoff"), py::arg("n"),
            "Constructs with base payoff and equal weights for n assets.")
        .def("weights", &AverageBasketPayoff::weights,
            py::return_value_policy::reference_internal,
            "Returns the weights.");

    // SpreadBasketPayoff
    py::class_<SpreadBasketPayoff, ext::shared_ptr<SpreadBasketPayoff>, BasketPayoff>(
        m, "SpreadBasketPayoff", "Payoff based on spread between two assets.")
        .def(py::init<ext::shared_ptr<Payoff>>(),
            py::arg("basePayoff"),
            "Constructs with base payoff.");

    // BasketOption
    py::class_<BasketOption, PyBasketOption, ext::shared_ptr<BasketOption>, MultiAssetOption>(
        m, "BasketOption", "Basket option on multiple assets.")
        .def(py::init<ext::shared_ptr<BasketPayoff>, ext::shared_ptr<Exercise>>(),
            py::arg("payoff"), py::arg("exercise"),
            "Constructs with basket payoff and exercise.");

    // BasketOption::engine - abstract base class, no constructor
    py::class_<BasketOption::engine, ext::shared_ptr<BasketOption::engine>, PricingEngine>(
        m, "BasketOptionEngine", "Base class for basket option engines.");
}
