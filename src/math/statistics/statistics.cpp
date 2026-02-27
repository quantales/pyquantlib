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
#include <ql/math/statistics/statistics.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::statistics(py::module_& m) {
    // Statistics = RiskStatistics = GenericRiskStatistics<GaussianStatistics>
    // Inherits: GeneralStatistics -> GaussianStatistics -> RiskStatistics
    // Bound as "Statistics" with all methods from the full hierarchy.
    py::class_<Statistics>(
        m, "Statistics",
        "Statistics tool with empirical-distribution risk measures.")
        .def(py::init<>())
        // GeneralStatistics inspectors
        .def("samples", &Statistics::samples,
            "Returns the number of samples collected.")
        .def("weightSum", &Statistics::weightSum,
            "Returns the sum of data weights.")
        .def("mean", &Statistics::mean,
            "Returns the mean.")
        .def("variance", &Statistics::variance,
            "Returns the variance.")
        .def("standardDeviation", &Statistics::standardDeviation,
            "Returns the standard deviation.")
        .def("errorEstimate", &Statistics::errorEstimate,
            "Returns the error estimate on the mean value.")
        .def("skewness", &Statistics::skewness,
            "Returns the skewness.")
        .def("kurtosis", &Statistics::kurtosis,
            "Returns the excess kurtosis.")
        .def("min", &Statistics::min,
            "Returns the minimum sample value.")
        .def("max", &Statistics::max,
            "Returns the maximum sample value.")
        .def("percentile", &Statistics::percentile,
            py::arg("y"),
            "Returns the y-th percentile.")
        .def("topPercentile", &Statistics::topPercentile,
            py::arg("y"),
            "Returns the y-th top percentile.")
        // GaussianStatistics methods
        .def("gaussianPercentile", &Statistics::gaussianPercentile,
            py::arg("percentile"),
            "Returns the gaussian-assumption percentile.")
        .def("gaussianTopPercentile", &Statistics::gaussianTopPercentile,
            py::arg("percentile"),
            "Returns the gaussian-assumption top percentile.")
        .def("gaussianPotentialUpside", &Statistics::gaussianPotentialUpside,
            py::arg("percentile"),
            "Returns the gaussian-assumption potential upside.")
        .def("gaussianValueAtRisk", &Statistics::gaussianValueAtRisk,
            py::arg("percentile"),
            "Returns the gaussian-assumption VaR.")
        .def("gaussianExpectedShortfall", &Statistics::gaussianExpectedShortfall,
            py::arg("percentile"),
            "Returns the gaussian-assumption expected shortfall.")
        .def("gaussianShortfall", &Statistics::gaussianShortfall,
            py::arg("target"),
            "Returns the gaussian-assumption shortfall probability.")
        .def("gaussianAverageShortfall", &Statistics::gaussianAverageShortfall,
            py::arg("target"),
            "Returns the gaussian-assumption averaged shortfallness.")
        .def("gaussianDownsideVariance", &Statistics::gaussianDownsideVariance,
            "Returns the gaussian-assumption downside variance.")
        .def("gaussianDownsideDeviation", &Statistics::gaussianDownsideDeviation,
            "Returns the gaussian-assumption downside deviation.")
        .def("gaussianRegret", &Statistics::gaussianRegret,
            py::arg("target"),
            "Returns the gaussian-assumption regret below target.")
        // RiskStatistics methods
        .def("semiVariance", &Statistics::semiVariance,
            "Returns the variance of observations below the mean.")
        .def("semiDeviation", &Statistics::semiDeviation,
            "Returns the semi deviation.")
        .def("downsideVariance", &Statistics::downsideVariance,
            "Returns the variance of observations below 0.")
        .def("downsideDeviation", &Statistics::downsideDeviation,
            "Returns the downside deviation.")
        .def("regret", &Statistics::regret,
            py::arg("target"),
            "Returns the variance of observations below target.")
        .def("potentialUpside", &Statistics::potentialUpside,
            py::arg("percentile"),
            "Returns the potential upside at a given percentile.")
        .def("valueAtRisk", &Statistics::valueAtRisk,
            py::arg("percentile"),
            "Returns the value-at-risk at a given percentile.")
        .def("expectedShortfall", &Statistics::expectedShortfall,
            py::arg("percentile"),
            "Returns the expected shortfall at a given percentile.")
        .def("shortfall", &Statistics::shortfall,
            py::arg("target"),
            "Returns the probability of missing the target.")
        .def("averageShortfall", &Statistics::averageShortfall,
            py::arg("target"),
            "Returns the averaged shortfallness below target.")
        // Modifiers
        .def("add", &Statistics::add,
            py::arg("value"),
            py::arg("weight") = 1.0,
            "Adds a datum to the set, possibly with a weight.")
        .def("addSequence",
            [](Statistics& self, const std::vector<Real>& values) {
                self.addSequence(values.begin(), values.end());
            },
            py::arg("values"),
            "Adds a sequence of data to the set.")
        .def("addSequence",
            [](Statistics& self, const std::vector<Real>& values,
               const std::vector<Real>& weights) {
                self.addSequence(values.begin(), values.end(),
                                 weights.begin());
            },
            py::arg("values"),
            py::arg("weights"),
            "Adds a sequence of data with weights.")
        .def("reset", &Statistics::reset,
            "Resets the data to a null set.")
        .def("sort", &Statistics::sort,
            "Sorts the data set in increasing order.");
}
