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
#include "pyquantlib/null_utils.h"
#include <ql/pricingengines/basket/mcamericanbasketengine.hpp>
#include <ql/processes/stochasticprocessarray.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::mcamericanbasketengine(py::module_& m) {
    m.def("MCAmericanBasketEngine",
        [](const ext::shared_ptr<StochasticProcessArray>& process,
           const std::string& rngType,
           py::object timeSteps,
           py::object timeStepsPerYear,
           bool brownianBridge,
           bool antitheticVariate,
           py::object requiredSamples,
           py::object requiredTolerance,
           py::object maxSamples,
           BigNatural seed,
           py::object calibrationSamples,
           Size polynomialOrder) -> ext::shared_ptr<PricingEngine> {

            Size timeStepsVal = from_python_with_null<Size>(timeSteps);
            Size timeStepsPerYearVal = from_python_with_null<Size>(timeStepsPerYear);
            Size requiredSamplesVal = from_python_with_null<Size>(requiredSamples);
            Real requiredToleranceVal = from_python_with_null<Real>(requiredTolerance);
            Size maxSamplesVal = from_python_with_null<Size>(maxSamples);
            Size calibrationSamplesVal = from_python_with_null<Size>(calibrationSamples);

            if (rngType == "lowdiscrepancy") {
                auto maker = MakeMCAmericanBasketEngine<LowDiscrepancy>(process);
                if (!is_null<Size>(timeSteps)) maker.withSteps(timeStepsVal);
                if (!is_null<Size>(timeStepsPerYear)) maker.withStepsPerYear(timeStepsPerYearVal);
                if (brownianBridge) maker.withBrownianBridge(brownianBridge);
                if (antitheticVariate) maker.withAntitheticVariate(antitheticVariate);
                if (!is_null<Size>(requiredSamples)) maker.withSamples(requiredSamplesVal);
                if (!is_null<Real>(requiredTolerance)) maker.withAbsoluteTolerance(requiredToleranceVal);
                if (!is_null<Size>(maxSamples)) maker.withMaxSamples(maxSamplesVal);
                if (seed != 0) maker.withSeed(seed);
                if (!is_null<Size>(calibrationSamples)) maker.withCalibrationSamples(calibrationSamplesVal);
                maker.withPolynomialOrder(polynomialOrder);
                return static_cast<ext::shared_ptr<PricingEngine>>(maker);
            } else {
                auto maker = MakeMCAmericanBasketEngine<PseudoRandom>(process);
                if (!is_null<Size>(timeSteps)) maker.withSteps(timeStepsVal);
                if (!is_null<Size>(timeStepsPerYear)) maker.withStepsPerYear(timeStepsPerYearVal);
                if (brownianBridge) maker.withBrownianBridge(brownianBridge);
                if (antitheticVariate) maker.withAntitheticVariate(antitheticVariate);
                if (!is_null<Size>(requiredSamples)) maker.withSamples(requiredSamplesVal);
                if (!is_null<Real>(requiredTolerance)) maker.withAbsoluteTolerance(requiredToleranceVal);
                if (!is_null<Size>(maxSamples)) maker.withMaxSamples(maxSamplesVal);
                if (seed != 0) maker.withSeed(seed);
                if (!is_null<Size>(calibrationSamples)) maker.withCalibrationSamples(calibrationSamplesVal);
                maker.withPolynomialOrder(polynomialOrder);
                return static_cast<ext::shared_ptr<PricingEngine>>(maker);
            }
        },
        py::arg("process"),
        py::arg("rngType") = "pseudorandom",
        py::arg("timeSteps") = py::none(),
        py::arg("timeStepsPerYear") = py::none(),
        py::arg("brownianBridge") = false,
        py::arg("antitheticVariate") = false,
        py::arg("requiredSamples") = py::none(),
        py::arg("requiredTolerance") = py::none(),
        py::arg("maxSamples") = py::none(),
        py::arg("seed") = 0,
        py::arg("calibrationSamples") = py::none(),
        py::arg("polynomialOrder") = 2,
        "Monte Carlo American basket option engine (Longstaff-Schwartz).");
}
