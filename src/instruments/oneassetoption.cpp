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
#include <ql/instruments/oneassetoption.hpp>
#include <ql/option.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::oneassetoption(py::module_& m) {
    py::module_ base = m.def_submodule("base", "Abstract base classes");

    // OneAssetOption ABC
    auto cls = py::class_<OneAssetOption, PyOneAssetOption,
                            ext::shared_ptr<OneAssetOption>, Option>(
        base, "OneAssetOption",
        "Abstract base class for options on a single asset.")
        .def(py::init<ext::shared_ptr<Payoff>, ext::shared_ptr<Exercise>>(),
             py::arg("payoff"), py::arg("exercise"))
        .def("delta", &OneAssetOption::delta,
            "Returns delta sensitivity.")
        .def("deltaForward", &OneAssetOption::deltaForward,
            "Returns forward delta.")
        .def("elasticity", &OneAssetOption::elasticity,
            "Returns elasticity (leverage).")
        .def("gamma", &OneAssetOption::gamma,
            "Returns gamma sensitivity.")
        .def("theta", &OneAssetOption::theta,
            "Returns theta sensitivity.")
        .def("thetaPerDay", &OneAssetOption::thetaPerDay,
            "Returns theta per day.")
        .def("vega", &OneAssetOption::vega,
            "Returns vega sensitivity.")
        .def("rho", &OneAssetOption::rho,
            "Returns rho sensitivity.")
        .def("dividendRho", &OneAssetOption::dividendRho,
            "Returns dividend rho sensitivity.")
        .def("strikeSensitivity", &OneAssetOption::strikeSensitivity,
            "Returns strike sensitivity.")
        .def("itmCashProbability", &OneAssetOption::itmCashProbability,
            "Returns probability of finishing in the money.");

    // OneAssetOption::results nested class
    py::class_<OneAssetOption::results, Instrument::results,
               Greeks, MoreGreeks, ext::shared_ptr<OneAssetOption::results>>(
        cls, "results",
        "Results from one-asset option pricing.")
        .def(py::init<>())
        .def("reset", &OneAssetOption::results::reset,
            "Resets all results.");

    // GenericEngine<OneAssetOption::arguments, OneAssetOption::results>
    using OneAssetGenericEngine = GenericEngine<OneAssetOption::arguments,
                                                 OneAssetOption::results>;

    py::class_<OneAssetGenericEngine, PyOneAssetGenericEngine,
               ext::shared_ptr<OneAssetGenericEngine>, PricingEngine, Observer>(
        base, "OneAssetOptionGenericEngine",
        "Generic base engine for one-asset options.")
        .def(py::init_alias<>());

    // OneAssetOption::engine
    py::class_<OneAssetOption::engine, PyOneAssetOptionEngine,
               ext::shared_ptr<OneAssetOption::engine>, OneAssetGenericEngine>(
        cls, "engine",
        "Pricing engine for one-asset options.")
        .def(py::init_alias<>());
}
