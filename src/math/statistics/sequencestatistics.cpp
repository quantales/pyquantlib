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
#include <ql/math/statistics/sequencestatistics.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::sequencestatistics(py::module_& m) {
    // SequenceStatistics = GenericSequenceStatistics<Statistics>
    py::class_<SequenceStatistics>(
        m, "SequenceStatistics",
        "N-dimensional statistics tool with covariance and correlation.")
        .def(py::init<Size>(),
            py::arg("dimension") = 0,
            "Constructs with given dimension (0 for auto-detection).")
        // Inspectors
        .def("size", &SequenceStatistics::size,
            "Returns the dimension.")
        .def("samples", &SequenceStatistics::samples,
            "Returns the number of samples collected.")
        .def("weightSum", &SequenceStatistics::weightSum,
            "Returns the sum of data weights.")
        // Covariance and correlation
        .def("covariance", &SequenceStatistics::covariance,
            "Returns the covariance matrix.")
        .def("correlation", &SequenceStatistics::correlation,
            "Returns the correlation matrix.")
        // N-D inspectors (void argument)
        .def("mean", &SequenceStatistics::mean,
            "Returns the mean for each dimension.")
        .def("variance", &SequenceStatistics::variance,
            "Returns the variance for each dimension.")
        .def("standardDeviation", &SequenceStatistics::standardDeviation,
            "Returns the standard deviation for each dimension.")
        .def("downsideVariance", &SequenceStatistics::downsideVariance,
            "Returns the downside variance for each dimension.")
        .def("downsideDeviation", &SequenceStatistics::downsideDeviation,
            "Returns the downside deviation for each dimension.")
        .def("semiVariance", &SequenceStatistics::semiVariance,
            "Returns the semi variance for each dimension.")
        .def("semiDeviation", &SequenceStatistics::semiDeviation,
            "Returns the semi deviation for each dimension.")
        .def("errorEstimate", &SequenceStatistics::errorEstimate,
            "Returns the error estimate for each dimension.")
        .def("skewness", &SequenceStatistics::skewness,
            "Returns the skewness for each dimension.")
        .def("kurtosis", &SequenceStatistics::kurtosis,
            "Returns the kurtosis for each dimension.")
        .def("min", &SequenceStatistics::min,
            "Returns the minimum for each dimension.")
        .def("max", &SequenceStatistics::max,
            "Returns the maximum for each dimension.")
        // N-D inspectors (single argument)
        .def("gaussianPercentile", &SequenceStatistics::gaussianPercentile,
            py::arg("y"),
            "Returns the gaussian percentile for each dimension.")
        .def("percentile", &SequenceStatistics::percentile,
            py::arg("y"),
            "Returns the percentile for each dimension.")
        .def("gaussianPotentialUpside", &SequenceStatistics::gaussianPotentialUpside,
            py::arg("percentile"),
            "Returns the gaussian potential upside for each dimension.")
        .def("potentialUpside", &SequenceStatistics::potentialUpside,
            py::arg("percentile"),
            "Returns the potential upside for each dimension.")
        .def("gaussianValueAtRisk", &SequenceStatistics::gaussianValueAtRisk,
            py::arg("percentile"),
            "Returns the gaussian VaR for each dimension.")
        .def("valueAtRisk", &SequenceStatistics::valueAtRisk,
            py::arg("percentile"),
            "Returns the VaR for each dimension.")
        .def("gaussianExpectedShortfall", &SequenceStatistics::gaussianExpectedShortfall,
            py::arg("percentile"),
            "Returns the gaussian expected shortfall for each dimension.")
        .def("expectedShortfall", &SequenceStatistics::expectedShortfall,
            py::arg("percentile"),
            "Returns the expected shortfall for each dimension.")
        .def("regret", &SequenceStatistics::regret,
            py::arg("target"),
            "Returns the regret for each dimension.")
        .def("gaussianShortfall", &SequenceStatistics::gaussianShortfall,
            py::arg("target"),
            "Returns the gaussian shortfall for each dimension.")
        .def("shortfall", &SequenceStatistics::shortfall,
            py::arg("target"),
            "Returns the shortfall for each dimension.")
        .def("gaussianAverageShortfall", &SequenceStatistics::gaussianAverageShortfall,
            py::arg("target"),
            "Returns the gaussian average shortfall for each dimension.")
        .def("averageShortfall", &SequenceStatistics::averageShortfall,
            py::arg("target"),
            "Returns the average shortfall for each dimension.")
        // Modifiers
        .def("add",
            [](SequenceStatistics& self,
               const std::vector<Real>& sample, Real weight) {
                self.add(sample, weight);
            },
            py::arg("sample"),
            py::arg("weight") = 1.0,
            "Adds an N-dimensional sample, possibly with a weight.")
        .def("reset", &SequenceStatistics::reset,
            py::arg("dimension") = 0,
            "Resets the data, optionally with a new dimension.");
}
