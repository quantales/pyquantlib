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
#include <ql/methods/montecarlo/pathgenerator.hpp>
#include <ql/math/randomnumbers/inversecumulativersg.hpp>
#include <ql/math/randomnumbers/randomsequencegenerator.hpp>
#include <ql/math/randomnumbers/mt19937uniformrng.hpp>
#include <ql/math/randomnumbers/sobolrsg.hpp>
#include <ql/math/distributions/normaldistribution.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

using GaussianRandomSequenceGenerator =
    InverseCumulativeRsg<RandomSequenceGenerator<MersenneTwisterUniformRng>,
                         InverseCumulativeNormal>;
using GaussianLowDiscrepancySequenceGenerator =
    InverseCumulativeRsg<SobolRsg, InverseCumulativeNormal>;

using GaussianPathGenerator = PathGenerator<GaussianRandomSequenceGenerator>;
using GaussianSobolPathGenerator =
    PathGenerator<GaussianLowDiscrepancySequenceGenerator>;

void ql_methods::pathgenerator(py::module_& m) {
    py::class_<GaussianPathGenerator>(m, "GaussianPathGenerator",
        "Single-factor path generator using pseudo-random Gaussian variates.")
        .def(py::init<const ext::shared_ptr<StochasticProcess>&,
                       Time, Size, GaussianRandomSequenceGenerator, bool>(),
            py::arg("process"), py::arg("length"), py::arg("timeSteps"),
            py::arg("generator"), py::arg("brownianBridge"),
            "Constructs from process, time length, steps, and generator.")
        .def(py::init<const ext::shared_ptr<StochasticProcess>&,
                       TimeGrid, GaussianRandomSequenceGenerator, bool>(),
            py::arg("process"), py::arg("timeGrid"),
            py::arg("generator"), py::arg("brownianBridge"),
            "Constructs from process, time grid, and generator.")
        .def("next", [](const GaussianPathGenerator& g) { return g.next(); },
            "Generates the next path sample.")
        .def("antithetic",
            [](const GaussianPathGenerator& g) { return g.antithetic(); },
            "Generates the antithetic path sample.")
        .def("size", &GaussianPathGenerator::size,
            "Generator dimensionality.")
        .def("timeGrid", &GaussianPathGenerator::timeGrid,
            py::return_value_policy::reference_internal,
            "Returns the underlying time grid.");

    py::class_<GaussianSobolPathGenerator>(m, "GaussianSobolPathGenerator",
        "Single-factor path generator using Sobol low-discrepancy variates.")
        .def(py::init<const ext::shared_ptr<StochasticProcess>&,
                       Time, Size, GaussianLowDiscrepancySequenceGenerator,
                       bool>(),
            py::arg("process"), py::arg("length"), py::arg("timeSteps"),
            py::arg("generator"), py::arg("brownianBridge"),
            "Constructs from process, time length, steps, and generator.")
        .def(py::init<const ext::shared_ptr<StochasticProcess>&,
                       TimeGrid, GaussianLowDiscrepancySequenceGenerator,
                       bool>(),
            py::arg("process"), py::arg("timeGrid"),
            py::arg("generator"), py::arg("brownianBridge"),
            "Constructs from process, time grid, and generator.")
        .def("next",
            [](const GaussianSobolPathGenerator& g) { return g.next(); },
            "Generates the next path sample.")
        .def("antithetic",
            [](const GaussianSobolPathGenerator& g) { return g.antithetic(); },
            "Generates the antithetic path sample.")
        .def("size", &GaussianSobolPathGenerator::size,
            "Generator dimensionality.")
        .def("timeGrid", &GaussianSobolPathGenerator::timeGrid,
            py::return_value_policy::reference_internal,
            "Returns the underlying time grid.");
}
