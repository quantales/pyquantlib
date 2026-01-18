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
#include <ql/pricingengines/basket/mceuropeanbasketengine.hpp>
#include <ql/processes/stochasticprocessarray.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::mceuropeanbasketengine(py::module_& m) {

    // MCEuropeanBasketEngine with PseudoRandom
    using MCEuropeanBasketEnginePR = MCEuropeanBasketEngine<PseudoRandom>;
    py::class_<MCEuropeanBasketEnginePR, ext::shared_ptr<MCEuropeanBasketEnginePR>, PricingEngine>(
        m, "MCEuropeanBasketEngine",
        "Monte Carlo pricing engine for European basket options (pseudo-random).")
        .def(py::init([](ext::shared_ptr<StochasticProcessArray> process,
                         Size timeSteps,
                         Size timeStepsPerYear,
                         bool brownianBridge,
                         bool antitheticVariate,
                         Size requiredSamples,
                         Real requiredTolerance,
                         Size maxSamples,
                         BigNatural seed) {
                return ext::make_shared<MCEuropeanBasketEnginePR>(
                    process,
                    timeSteps,
                    timeStepsPerYear,
                    brownianBridge,
                    antitheticVariate,
                    requiredSamples,
                    requiredTolerance,
                    maxSamples,
                    seed);
            }),
            py::arg("process"),
            py::arg("timeSteps") = Null<Size>(),
            py::arg("timeStepsPerYear") = Null<Size>(),
            py::arg("brownianBridge") = false,
            py::arg("antitheticVariate") = false,
            py::arg("requiredSamples") = Null<Size>(),
            py::arg("requiredTolerance") = Null<Real>(),
            py::arg("maxSamples") = Null<Size>(),
            py::arg("seed") = BigNatural(0),
            "Constructs MC European basket engine with pseudo-random numbers.");

    // MCEuropeanBasketEngine with LowDiscrepancy (Sobol)
    using MCEuropeanBasketEngineLD = MCEuropeanBasketEngine<LowDiscrepancy>;
    py::class_<MCEuropeanBasketEngineLD, ext::shared_ptr<MCEuropeanBasketEngineLD>, PricingEngine>(
        m, "MCLDEuropeanBasketEngine",
        "Monte Carlo pricing engine for European basket options (low-discrepancy/Sobol).")
        .def(py::init([](ext::shared_ptr<StochasticProcessArray> process,
                         Size timeSteps,
                         Size timeStepsPerYear,
                         bool brownianBridge,
                         bool antitheticVariate,
                         Size requiredSamples,
                         Real requiredTolerance,
                         Size maxSamples,
                         BigNatural seed) {
                return ext::make_shared<MCEuropeanBasketEngineLD>(
                    process,
                    timeSteps,
                    timeStepsPerYear,
                    brownianBridge,
                    antitheticVariate,
                    requiredSamples,
                    requiredTolerance,
                    maxSamples,
                    seed);
            }),
            py::arg("process"),
            py::arg("timeSteps") = Null<Size>(),
            py::arg("timeStepsPerYear") = Null<Size>(),
            py::arg("brownianBridge") = false,
            py::arg("antitheticVariate") = false,
            py::arg("requiredSamples") = Null<Size>(),
            py::arg("requiredTolerance") = Null<Real>(),
            py::arg("maxSamples") = Null<Size>(),
            py::arg("seed") = BigNatural(0),
            "Constructs MC European basket engine with low-discrepancy sequences.");
}
