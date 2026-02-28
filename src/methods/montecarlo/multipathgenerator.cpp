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
#include <ql/methods/montecarlo/multipathgenerator.hpp>
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

using GaussianMultiPathGenerator =
    MultiPathGenerator<GaussianRandomSequenceGenerator>;
using GaussianSobolMultiPathGenerator =
    MultiPathGenerator<GaussianLowDiscrepancySequenceGenerator>;

void ql_methods::multipathgenerator(py::module_& m) {
    py::class_<GaussianMultiPathGenerator>(m, "GaussianMultiPathGenerator",
        "Multi-factor path generator using pseudo-random Gaussian variates.")
        .def(py::init<const ext::shared_ptr<StochasticProcess>&,
                       const TimeGrid&, GaussianRandomSequenceGenerator,
                       bool>(),
            py::arg("process"), py::arg("timeGrid"),
            py::arg("generator"), py::arg("brownianBridge") = false,
            "Constructs from process, time grid, and generator.")
        .def("next",
            [](const GaussianMultiPathGenerator& g) { return g.next(); },
            "Generates the next multi-path sample.")
        .def("antithetic",
            [](const GaussianMultiPathGenerator& g) { return g.antithetic(); },
            "Generates the antithetic multi-path sample.");

    py::class_<GaussianSobolMultiPathGenerator>(
        m, "GaussianSobolMultiPathGenerator",
        "Multi-factor path generator using Sobol low-discrepancy variates.")
        .def(py::init<const ext::shared_ptr<StochasticProcess>&,
                       const TimeGrid&,
                       GaussianLowDiscrepancySequenceGenerator, bool>(),
            py::arg("process"), py::arg("timeGrid"),
            py::arg("generator"), py::arg("brownianBridge") = false,
            "Constructs from process, time grid, and generator.")
        .def("next",
            [](const GaussianSobolMultiPathGenerator& g) { return g.next(); },
            "Generates the next multi-path sample.")
        .def("antithetic",
            [](const GaussianSobolMultiPathGenerator& g) {
                return g.antithetic();
            },
            "Generates the antithetic multi-path sample.");
}
