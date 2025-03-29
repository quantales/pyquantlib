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
#include <ql/pricingengines/vanilla/analytichestonengine.hpp>
#include <ql/models/equity/hestonmodel.hpp>
#include <ql/instruments/vanillaoption.hpp>
#include <ql/instruments/payoffs.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::analytichestonengine(py::module_& m) {
    // ComplexLogFormula enum
    py::enum_<AnalyticHestonEngine::ComplexLogFormula>(m, "ComplexLogFormula",
        "Formula for complex logarithm in Heston integration.")
        .value("Gatheral", AnalyticHestonEngine::Gatheral)
        .value("BranchCorrection", AnalyticHestonEngine::BranchCorrection)
        .value("AndersenPiterbarg", AnalyticHestonEngine::AndersenPiterbarg)
        .value("AndersenPiterbargOptCV", AnalyticHestonEngine::AndersenPiterbargOptCV)
        .value("AsymptoticChF", AnalyticHestonEngine::AsymptoticChF)
        .value("AngledContour", AnalyticHestonEngine::AngledContour)
        .value("AngledContourNoCV", AnalyticHestonEngine::AngledContourNoCV)
        .value("OptimalCV", AnalyticHestonEngine::OptimalCV);

    // Integration nested class
    py::class_<AnalyticHestonEngine::Integration>(m, "Integration",
        "Integration methods for Heston engine.")
        .def_static("gaussLaguerre",
            &AnalyticHestonEngine::Integration::gaussLaguerre,
            py::arg("integrationOrder") = 128)
        .def_static("gaussLegendre",
            &AnalyticHestonEngine::Integration::gaussLegendre,
            py::arg("integrationOrder") = 128)
        .def_static("gaussChebyshev",
            &AnalyticHestonEngine::Integration::gaussChebyshev,
            py::arg("integrationOrder") = 128)
        .def_static("gaussChebyshev2nd",
            &AnalyticHestonEngine::Integration::gaussChebyshev2nd,
            py::arg("integrationOrder") = 128)
        .def_static("gaussLobatto",
            &AnalyticHestonEngine::Integration::gaussLobatto,
            py::arg("relTolerance"), py::arg("absTolerance"),
            py::arg("maxEvaluations") = 1000,
            py::arg("useConvergenceEstimate") = false)
        .def_static("gaussKronrod",
            &AnalyticHestonEngine::Integration::gaussKronrod,
            py::arg("absTolerance"), py::arg("maxEvaluations") = 1000)
        .def_static("simpson",
            &AnalyticHestonEngine::Integration::simpson,
            py::arg("absTolerance"), py::arg("maxEvaluations") = 1000)
        .def_static("trapezoid",
            &AnalyticHestonEngine::Integration::trapezoid,
            py::arg("absTolerance"), py::arg("maxEvaluations") = 1000)
        .def_static("discreteSimpson",
            &AnalyticHestonEngine::Integration::discreteSimpson,
            py::arg("evaluations") = 1000)
        .def_static("discreteTrapezoid",
            &AnalyticHestonEngine::Integration::discreteTrapezoid,
            py::arg("evaluations") = 1000)
        .def_static("expSinh",
            &AnalyticHestonEngine::Integration::expSinh,
            py::arg("relTolerance") = 1e-8)
        .def("numberOfEvaluations",
            &AnalyticHestonEngine::Integration::numberOfEvaluations)
        .def("isAdaptiveIntegration",
            &AnalyticHestonEngine::Integration::isAdaptiveIntegration);

    // AnalyticHestonEngine - GenericHestonModelEngine is defined in trampolines.h
    py::class_<AnalyticHestonEngine, GenericHestonModelEngine,
               ext::shared_ptr<AnalyticHestonEngine>>(
        m, "AnalyticHestonEngine",
        "Analytic pricing engine for Heston stochastic volatility model.")
        // Simple constructor with adaptive Gauss-Lobatto
        .def(py::init<const ext::shared_ptr<HestonModel>&, Real, Size>(),
             py::arg("model"), py::arg("relTolerance"), py::arg("maxEvaluations"),
            "Constructs with adaptive Gauss-Lobatto integration.")
        // Constructor with Laguerre integration order
        .def(py::init<const ext::shared_ptr<HestonModel>&, Size>(),
             py::arg("model"), py::arg("integrationOrder") = 144,
            "Constructs with Gauss-Laguerre integration.")
        // Full control constructor
        .def(py::init<const ext::shared_ptr<HestonModel>&,
                      AnalyticHestonEngine::ComplexLogFormula,
                      const AnalyticHestonEngine::Integration&, Real, Real>(),
             py::arg("model"), py::arg("cpxLog"), py::arg("integration"),
             py::arg("andersenPiterbargEpsilon") = 1e-25,
             py::arg("alpha") = -0.5,
            "Constructs with full control over integration method.")
        .def("numberOfEvaluations", &AnalyticHestonEngine::numberOfEvaluations,
            "Returns number of integration evaluations.")
        .def("priceVanillaPayoff",
            py::overload_cast<const ext::shared_ptr<PlainVanillaPayoff>&, Time>(
                &AnalyticHestonEngine::priceVanillaPayoff, py::const_),
            py::arg("payoff"), py::arg("maturity"),
            "Prices vanilla payoff for given maturity.");
}
