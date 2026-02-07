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
#include <ql/pricingengines/asian/mc_discr_arith_av_price.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::mcdiscretearithmeticapengine(py::module_& m) {
    m.def("MCDiscreteArithmeticAPEngine",
        [](const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
           const std::string& rngType,
           bool brownianBridge,
           bool antitheticVariate,
           bool controlVariate,
           py::object requiredSamples,
           py::object requiredTolerance,
           py::object maxSamples,
           BigNatural seed) -> ext::shared_ptr<PricingEngine> {

            Size requiredSamplesVal = from_python_with_null<Size>(requiredSamples);
            Real requiredToleranceVal = from_python_with_null<Real>(requiredTolerance);
            Size maxSamplesVal = from_python_with_null<Size>(maxSamples);

            if (rngType == "lowdiscrepancy") {
                auto maker = MakeMCDiscreteArithmeticAPEngine<LowDiscrepancy>(process);
                if (brownianBridge) maker.withBrownianBridge(brownianBridge);
                if (antitheticVariate) maker.withAntitheticVariate(antitheticVariate);
                if (controlVariate) maker.withControlVariate(controlVariate);
                if (!is_null<Size>(requiredSamples)) maker.withSamples(requiredSamplesVal);
                if (!is_null<Real>(requiredTolerance)) maker.withAbsoluteTolerance(requiredToleranceVal);
                if (!is_null<Size>(maxSamples)) maker.withMaxSamples(maxSamplesVal);
                if (seed != 0) maker.withSeed(seed);
                return static_cast<ext::shared_ptr<PricingEngine>>(maker);
            } else {
                auto maker = MakeMCDiscreteArithmeticAPEngine<PseudoRandom>(process);
                if (brownianBridge) maker.withBrownianBridge(brownianBridge);
                if (antitheticVariate) maker.withAntitheticVariate(antitheticVariate);
                if (controlVariate) maker.withControlVariate(controlVariate);
                if (!is_null<Size>(requiredSamples)) maker.withSamples(requiredSamplesVal);
                if (!is_null<Real>(requiredTolerance)) maker.withAbsoluteTolerance(requiredToleranceVal);
                if (!is_null<Size>(maxSamples)) maker.withMaxSamples(maxSamplesVal);
                if (seed != 0) maker.withSeed(seed);
                return static_cast<ext::shared_ptr<PricingEngine>>(maker);
            }
        },
        py::arg("process"),
        py::arg("rngType") = "pseudorandom",
        py::arg("brownianBridge") = true,
        py::arg("antitheticVariate") = false,
        py::arg("controlVariate") = false,
        py::arg("requiredSamples") = py::none(),
        py::arg("requiredTolerance") = py::none(),
        py::arg("maxSamples") = py::none(),
        py::arg("seed") = 0,
        "Monte Carlo discrete arithmetic average price Asian engine.");
}
