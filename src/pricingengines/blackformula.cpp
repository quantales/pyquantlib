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
#include <ql/pricingengines/blackformula.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::blackformula(py::module_& m) {

    // Black 1976 formula (lognormal)
    m.def("blackFormula",
        py::overload_cast<Option::Type, Real, Real, Real, Real, Real>(
            &blackFormula),
        py::arg("optionType"),
        py::arg("strike"),
        py::arg("forward"),
        py::arg("stdDev"),
        py::arg("discount") = 1.0,
        py::arg("displacement") = 0.0,
        "Black 1976 formula. stdDev = volatility * sqrt(T).");

    // Black implied standard deviation
    m.def("blackFormulaImpliedStdDev",
        py::overload_cast<Option::Type, Real, Real, Real, Real, Real, Real, Real, Natural>(
            &blackFormulaImpliedStdDev),
        py::arg("optionType"),
        py::arg("strike"),
        py::arg("forward"),
        py::arg("blackPrice"),
        py::arg("discount") = 1.0,
        py::arg("displacement") = 0.0,
        py::arg("guess") = Null<Real>(),
        py::arg("accuracy") = 1.0e-6,
        py::arg("maxIterations") = 100,
        "Black 1976 implied standard deviation (volatility * sqrt(T)).");

    // Black implied standard deviation approximation (faster, no iteration)
    m.def("blackFormulaImpliedStdDevApproximation",
        py::overload_cast<Option::Type, Real, Real, Real, Real, Real>(
            &blackFormulaImpliedStdDevApproximation),
        py::arg("optionType"),
        py::arg("strike"),
        py::arg("forward"),
        py::arg("blackPrice"),
        py::arg("discount") = 1.0,
        py::arg("displacement") = 0.0,
        "Approximated Black implied stdDev (Corrado-Miller).");

    // Standard deviation derivative (vega building block)
    m.def("blackFormulaStdDevDerivative",
        py::overload_cast<Real, Real, Real, Real, Real>(
            &blackFormulaStdDevDerivative),
        py::arg("strike"),
        py::arg("forward"),
        py::arg("stdDev"),
        py::arg("discount") = 1.0,
        py::arg("displacement") = 0.0,
        "Black formula derivative w.r.t. stdDev. Vega = this * sqrt(T).");

    // Vol derivative (actual vega)
    m.def("blackFormulaVolDerivative",
        &blackFormulaVolDerivative,
        py::arg("strike"),
        py::arg("forward"),
        py::arg("stdDev"),
        py::arg("expiry"),
        py::arg("discount") = 1.0,
        py::arg("displacement") = 0.0,
        "Black formula derivative w.r.t. implied vol (vega).");

    // Forward derivative (delta building block)
    m.def("blackFormulaForwardDerivative",
        py::overload_cast<Option::Type, Real, Real, Real, Real, Real>(
            &blackFormulaForwardDerivative),
        py::arg("optionType"),
        py::arg("strike"),
        py::arg("forward"),
        py::arg("stdDev"),
        py::arg("discount") = 1.0,
        py::arg("displacement") = 0.0,
        "Black formula derivative w.r.t. forward.");

    // Cash ITM probability (N(d2))
    m.def("blackFormulaCashItmProbability",
        py::overload_cast<Option::Type, Real, Real, Real, Real>(
            &blackFormulaCashItmProbability),
        py::arg("optionType"),
        py::arg("strike"),
        py::arg("forward"),
        py::arg("stdDev"),
        py::arg("displacement") = 0.0,
        "Probability of finishing in the money N(d2).");

    // Asset ITM probability (N(d1))
    m.def("blackFormulaAssetItmProbability",
        py::overload_cast<Option::Type, Real, Real, Real, Real>(
            &blackFormulaAssetItmProbability),
        py::arg("optionType"),
        py::arg("strike"),
        py::arg("forward"),
        py::arg("stdDev"),
        py::arg("displacement") = 0.0,
        "Asset measure probability N(d1).");

    // Bachelier (normal) formula
    m.def("bachelierBlackFormula",
        py::overload_cast<Option::Type, Real, Real, Real, Real>(
            &bachelierBlackFormula),
        py::arg("optionType"),
        py::arg("strike"),
        py::arg("forward"),
        py::arg("stdDev"),
        py::arg("discount") = 1.0,
        "Bachelier (normal) formula. stdDev = absoluteVol * sqrt(T).");

    // Bachelier implied volatility
    m.def("bachelierBlackFormulaImpliedVol",
        &bachelierBlackFormulaImpliedVol,
        py::arg("optionType"),
        py::arg("strike"),
        py::arg("forward"),
        py::arg("tte"),
        py::arg("bachelierPrice"),
        py::arg("discount") = 1.0,
        "Bachelier implied volatility (exact, Jaeckel 2017).");

    // Bachelier stdDev derivative
    m.def("bachelierBlackFormulaStdDevDerivative",
        py::overload_cast<Real, Real, Real, Real>(
            &bachelierBlackFormulaStdDevDerivative),
        py::arg("strike"),
        py::arg("forward"),
        py::arg("stdDev"),
        py::arg("discount") = 1.0,
        "Bachelier formula derivative w.r.t. stdDev.");
}
