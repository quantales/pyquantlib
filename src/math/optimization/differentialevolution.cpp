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
#include <ql/math/optimization/differentialevolution.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::differentialevolution(py::module_& m) {
    using DE = DifferentialEvolution;
    using Config = DE::Configuration;

    // Strategy enum
    py::enum_<DE::Strategy>(m, "DEStrategy",
        "Differential evolution mutation strategy.")
        .value("Rand1Standard", DE::Rand1Standard)
        .value("BestMemberWithJitter", DE::BestMemberWithJitter)
        .value("CurrentToBest2Diffs", DE::CurrentToBest2Diffs)
        .value("Rand1DiffWithPerVectorDither", DE::Rand1DiffWithPerVectorDither)
        .value("Rand1DiffWithDither", DE::Rand1DiffWithDither)
        .value("EitherOrWithOptimalRecombination", DE::EitherOrWithOptimalRecombination)
        .value("Rand1SelfadaptiveWithRotation", DE::Rand1SelfadaptiveWithRotation);

    // CrossoverType enum
    py::enum_<DE::CrossoverType>(m, "DECrossoverType",
        "Differential evolution crossover type.")
        .value("Normal", DE::Normal)
        .value("Binomial", DE::Binomial)
        .value("Exponential", DE::Exponential);

    // Configuration class
    py::class_<Config>(m, "DEConfiguration",
        "Configuration for the differential evolution optimizer.")
        .def(py::init<>(), "Constructs with default settings.")
        .def_readwrite("strategy", &Config::strategy,
            "Mutation strategy.")
        .def_readwrite("crossoverType", &Config::crossoverType,
            "Crossover type.")
        .def_readwrite("populationMembers", &Config::populationMembers,
            "Number of population members.")
        .def_readwrite("stepsizeWeight", &Config::stepsizeWeight,
            "Step size weight (F).")
        .def_readwrite("crossoverProbability", &Config::crossoverProbability,
            "Crossover probability (CR).")
        .def_readwrite("seed", &Config::seed,
            "Random seed.")
        .def_readwrite("applyBounds", &Config::applyBounds,
            "Whether to apply bounds.")
        .def_readwrite("crossoverIsAdaptive", &Config::crossoverIsAdaptive,
            "Whether crossover is adaptive.")
        .def_readwrite("upperBound", &Config::upperBound,
            "Upper bounds for parameters.")
        .def_readwrite("lowerBound", &Config::lowerBound,
            "Lower bounds for parameters.")
        .def("withStrategy", &Config::withStrategy,
            py::arg("strategy"),
            py::return_value_policy::reference_internal,
            "Sets mutation strategy.")
        .def("withCrossoverType", &Config::withCrossoverType,
            py::arg("crossoverType"),
            py::return_value_policy::reference_internal,
            "Sets crossover type.")
        .def("withPopulationMembers", &Config::withPopulationMembers,
            py::arg("n"),
            py::return_value_policy::reference_internal,
            "Sets number of population members.")
        .def("withStepsizeWeight", &Config::withStepsizeWeight,
            py::arg("w"),
            py::return_value_policy::reference_internal,
            "Sets step size weight.")
        .def("withCrossoverProbability", &Config::withCrossoverProbability,
            py::arg("p"),
            py::return_value_policy::reference_internal,
            "Sets crossover probability.")
        .def("withSeed", &Config::withSeed,
            py::arg("seed"),
            py::return_value_policy::reference_internal,
            "Sets random seed.")
        .def("withBounds", &Config::withBounds,
            py::arg("b") = true,
            py::return_value_policy::reference_internal,
            "Sets whether to apply bounds.")
        .def("withAdaptiveCrossover", &Config::withAdaptiveCrossover,
            py::arg("b") = true,
            py::return_value_policy::reference_internal,
            "Sets whether crossover is adaptive.")
        .def("withUpperBound", &Config::withUpperBound,
            py::arg("u"),
            py::return_value_policy::reference_internal,
            "Sets upper bounds.")
        .def("withLowerBound", &Config::withLowerBound,
            py::arg("l"),
            py::return_value_policy::reference_internal,
            "Sets lower bounds.");

    // DifferentialEvolution optimizer
    py::class_<DE, OptimizationMethod, ext::shared_ptr<DE>>(
        m, "DifferentialEvolution",
        "Differential evolution global optimization method.")
        .def(py::init<const Config&>(),
            py::arg("configuration") = Config(),
            "Constructs with the given configuration.")
        .def("configuration", &DE::configuration,
            py::return_value_policy::reference_internal,
            "Returns the configuration.");
}
