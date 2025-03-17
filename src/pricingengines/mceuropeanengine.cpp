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
#include "pyquantlib/null_utils.h"
#include <ql/pricingengines/vanilla/mceuropeanengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/exercise.hpp>
#include <pybind11/pybind11.h>
#include <algorithm>
#include <cctype>

namespace py = pybind11;
using namespace QuantLib;

namespace {
    std::string to_lower(const std::string& s) {
        std::string result = s;
        std::transform(result.begin(), result.end(), result.begin(),
                       [](unsigned char c) { return std::tolower(c); });
        return result;
    }
}

void ql_pricingengines::mceuropeanengine(py::module_& m) {
    // Full constructor with all parameters
    m.def("MCEuropeanEngine",
        [](const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
           const std::string& rngType,
           py::object timeSteps,
           py::object timeStepsPerYear,
           bool brownianBridge,
           bool antitheticVariate,
           py::object requiredSamples,
           py::object requiredTolerance,
           py::object maxSamples,
           BigNatural seed) -> ext::shared_ptr<PricingEngine> {

            std::string lowerRngType = to_lower(rngType);

            Size timeStepsVal = from_python_with_null<Size>(timeSteps);
            Size timeStepsPerYearVal = from_python_with_null<Size>(timeStepsPerYear);
            Size requiredSamplesVal = from_python_with_null<Size>(requiredSamples);
            Real requiredToleranceVal = from_python_with_null<Real>(requiredTolerance);
            Size maxSamplesVal = from_python_with_null<Size>(maxSamples);

            if (lowerRngType == "pseudorandom") {
                auto maker = MakeMCEuropeanEngine<PseudoRandom>(process);

                if (!is_null<Size>(timeSteps)) maker.withSteps(timeStepsVal);
                if (!is_null<Size>(timeStepsPerYear)) maker.withStepsPerYear(timeStepsPerYearVal);
                if (brownianBridge) maker.withBrownianBridge(brownianBridge);
                if (antitheticVariate) maker.withAntitheticVariate(antitheticVariate);
                if (!is_null<Size>(requiredSamples)) maker.withSamples(requiredSamplesVal);
                if (!is_null<Real>(requiredTolerance)) maker.withAbsoluteTolerance(requiredToleranceVal);
                if (!is_null<Size>(maxSamples)) maker.withMaxSamples(maxSamplesVal);
                if (seed != 0) maker.withSeed(seed);

                return static_cast<ext::shared_ptr<PricingEngine>>(maker);

            } else if (lowerRngType == "lowdiscrepancy") {
                auto maker = MakeMCEuropeanEngine<LowDiscrepancy>(process);

                if (!is_null<Size>(timeSteps)) maker.withSteps(timeStepsVal);
                if (!is_null<Size>(timeStepsPerYear)) maker.withStepsPerYear(timeStepsPerYearVal);
                if (brownianBridge) maker.withBrownianBridge(brownianBridge);
                if (antitheticVariate) maker.withAntitheticVariate(antitheticVariate);
                if (!is_null<Size>(requiredSamples)) maker.withSamples(requiredSamplesVal);
                if (!is_null<Real>(requiredTolerance)) maker.withAbsoluteTolerance(requiredToleranceVal);
                if (!is_null<Size>(maxSamples)) maker.withMaxSamples(maxSamplesVal);
                if (seed != 0) maker.withSeed(seed);

                return static_cast<ext::shared_ptr<PricingEngine>>(maker);

            } else {
                throw std::runtime_error(
                    "Unsupported RNG type. Use 'pseudorandom' or 'lowdiscrepancy'.");
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
        "Monte Carlo European option pricing engine.\n\n"
        "Parameters:\n"
        "  process: Black-Scholes process\n"
        "  rngType: 'pseudorandom' or 'lowdiscrepancy'\n"
        "  timeSteps: Number of time steps\n"
        "  timeStepsPerYear: Time steps per year (alternative to timeSteps)\n"
        "  brownianBridge: Use Brownian bridge\n"
        "  antitheticVariate: Use antithetic variates\n"
        "  requiredSamples: Number of samples\n"
        "  requiredTolerance: Target tolerance (alternative to requiredSamples)\n"
        "  maxSamples: Maximum samples\n"
        "  seed: Random seed (0 for random)");
}
