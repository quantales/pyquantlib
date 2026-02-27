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
#include <ql/pricingengines/vanilla/mcamericanengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
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

void ql_pricingengines::mcamericanengine(py::module_& m) {
    // LsmBasisSystem::PolynomialType enum is bound in lsmbasissystem.cpp

    // MCAmericanEngine factory function
    m.def("MCAmericanEngine",
        [](const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
           const std::string& rngType,
           py::object timeSteps,
           py::object timeStepsPerYear,
           bool antitheticVariate,
           bool controlVariate,
           py::object requiredSamples,
           py::object requiredTolerance,
           py::object maxSamples,
           BigNatural seed,
           Size polynomialOrder,
           LsmBasisSystem::PolynomialType polynomialType,
           Size calibrationSamples) -> ext::shared_ptr<PricingEngine> {

            std::string lowerRngType = to_lower(rngType);

            Size timeStepsVal = from_python_with_null<Size>(timeSteps);
            Size timeStepsPerYearVal = from_python_with_null<Size>(timeStepsPerYear);
            Size requiredSamplesVal = from_python_with_null<Size>(requiredSamples);
            Real requiredToleranceVal = from_python_with_null<Real>(requiredTolerance);
            Size maxSamplesVal = from_python_with_null<Size>(maxSamples);

            if (lowerRngType == "pseudorandom") {
                auto maker = MakeMCAmericanEngine<PseudoRandom>(process);

                if (!is_null<Size>(timeSteps)) maker.withSteps(timeStepsVal);
                if (!is_null<Size>(timeStepsPerYear)) maker.withStepsPerYear(timeStepsPerYearVal);
                if (antitheticVariate) maker.withAntitheticVariate(antitheticVariate);
                if (controlVariate) maker.withControlVariate(controlVariate);
                if (!is_null<Size>(requiredSamples)) maker.withSamples(requiredSamplesVal);
                if (!is_null<Real>(requiredTolerance)) maker.withAbsoluteTolerance(requiredToleranceVal);
                if (!is_null<Size>(maxSamples)) maker.withMaxSamples(maxSamplesVal);
                if (seed != 0) maker.withSeed(seed);
                maker.withPolynomialOrder(polynomialOrder);
                maker.withBasisSystem(polynomialType);
                maker.withCalibrationSamples(calibrationSamples);

                return static_cast<ext::shared_ptr<PricingEngine>>(maker);

            } else if (lowerRngType == "lowdiscrepancy") {
                auto maker = MakeMCAmericanEngine<LowDiscrepancy>(process);

                if (!is_null<Size>(timeSteps)) maker.withSteps(timeStepsVal);
                if (!is_null<Size>(timeStepsPerYear)) maker.withStepsPerYear(timeStepsPerYearVal);
                if (antitheticVariate) maker.withAntitheticVariate(antitheticVariate);
                if (controlVariate) maker.withControlVariate(controlVariate);
                if (!is_null<Size>(requiredSamples)) maker.withSamples(requiredSamplesVal);
                if (!is_null<Real>(requiredTolerance)) maker.withAbsoluteTolerance(requiredToleranceVal);
                if (!is_null<Size>(maxSamples)) maker.withMaxSamples(maxSamplesVal);
                if (seed != 0) maker.withSeed(seed);
                maker.withPolynomialOrder(polynomialOrder);
                maker.withBasisSystem(polynomialType);
                maker.withCalibrationSamples(calibrationSamples);

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
        py::arg("antitheticVariate") = false,
        py::arg("controlVariate") = false,
        py::arg("requiredSamples") = py::none(),
        py::arg("requiredTolerance") = py::none(),
        py::arg("maxSamples") = py::none(),
        py::arg("seed") = 0,
        py::arg("polynomialOrder") = 2,
        py::arg("polynomialType") = LsmBasisSystem::Monomial,
        py::arg("calibrationSamples") = 2048,
        "Monte Carlo American option pricing engine (Longstaff-Schwartz).\n\n"
        "Parameters:\n"
        "  process: Black-Scholes process\n"
        "  rngType: 'pseudorandom' or 'lowdiscrepancy'\n"
        "  timeSteps: Number of time steps\n"
        "  timeStepsPerYear: Time steps per year (alternative to timeSteps)\n"
        "  antitheticVariate: Use antithetic variates\n"
        "  controlVariate: Use control variate (European option)\n"
        "  requiredSamples: Number of samples\n"
        "  requiredTolerance: Target tolerance (alternative to requiredSamples)\n"
        "  maxSamples: Maximum samples\n"
        "  seed: Random seed (0 for random)\n"
        "  polynomialOrder: Order of regression polynomial\n"
        "  polynomialType: Polynomial basis type (Monomial, Laguerre, etc.)\n"
        "  calibrationSamples: Samples for regression calibration");
}
