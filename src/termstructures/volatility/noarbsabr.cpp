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
#include <ql/experimental/volatility/noarbsabr.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::noarbsabr(py::module_& m) {
    py::class_<NoArbSabrModel, ext::shared_ptr<NoArbSabrModel>>(
        m, "NoArbSabrModel",
        "No-arbitrage SABR model (Doust, 2012). Provides arbitrage-free "
        "option prices, digital prices, and density.")
        .def(py::init<Real, Real, Real, Real, Real, Real>(),
            py::arg("expiryTime"),
            py::arg("forward"),
            py::arg("alpha"),
            py::arg("beta"),
            py::arg("nu"),
            py::arg("rho"),
            "Constructs a no-arbitrage SABR model.")
        .def("optionPrice", &NoArbSabrModel::optionPrice,
            py::arg("strike"),
            "Returns the (undiscounted) call option price for the given strike.")
        .def("digitalOptionPrice", &NoArbSabrModel::digitalOptionPrice,
            py::arg("strike"),
            "Returns the (undiscounted) digital call option price.")
        .def("density", &NoArbSabrModel::density,
            py::arg("strike"),
            "Returns the probability density at the given strike.")
        .def("forward", &NoArbSabrModel::forward,
            "Returns the external (input) forward rate.")
        .def("numericalForward", &NoArbSabrModel::numericalForward,
            "Returns the model-implied numerical forward.")
        .def("expiryTime", &NoArbSabrModel::expiryTime)
        .def("alpha", &NoArbSabrModel::alpha)
        .def("beta", &NoArbSabrModel::beta)
        .def("nu", &NoArbSabrModel::nu)
        .def("rho", &NoArbSabrModel::rho)
        .def("absorptionProbability", &NoArbSabrModel::absorptionProbability,
            "Returns the probability of absorption at zero.");
}
