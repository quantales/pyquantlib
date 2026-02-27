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
#include <ql/math/statistics/incrementalstatistics.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::incrementalstatistics(py::module_& m) {
    py::class_<IncrementalStatistics>(
        m, "IncrementalStatistics",
        "Statistics tool based on incremental accumulation (boost accumulators).")
        .def(py::init<>())
        // Inspectors
        .def("samples", &IncrementalStatistics::samples,
            "Returns the number of samples collected.")
        .def("weightSum", &IncrementalStatistics::weightSum,
            "Returns the sum of data weights.")
        .def("mean", &IncrementalStatistics::mean,
            "Returns the mean.")
        .def("variance", &IncrementalStatistics::variance,
            "Returns the variance.")
        .def("standardDeviation", &IncrementalStatistics::standardDeviation,
            "Returns the standard deviation.")
        .def("errorEstimate", &IncrementalStatistics::errorEstimate,
            "Returns the error estimate on the mean value.")
        .def("skewness", &IncrementalStatistics::skewness,
            "Returns the skewness.")
        .def("kurtosis", &IncrementalStatistics::kurtosis,
            "Returns the excess kurtosis.")
        .def("min", &IncrementalStatistics::min,
            "Returns the minimum sample value.")
        .def("max", &IncrementalStatistics::max,
            "Returns the maximum sample value.")
        .def("downsideSamples", &IncrementalStatistics::downsideSamples,
            "Returns the number of negative samples collected.")
        .def("downsideWeightSum", &IncrementalStatistics::downsideWeightSum,
            "Returns the sum of data weights for negative samples.")
        .def("downsideVariance", &IncrementalStatistics::downsideVariance,
            "Returns the downside variance.")
        .def("downsideDeviation", &IncrementalStatistics::downsideDeviation,
            "Returns the downside deviation.")
        // Modifiers
        .def("add", &IncrementalStatistics::add,
            py::arg("value"),
            py::arg("weight") = 1.0,
            "Adds a datum to the set, possibly with a weight.")
        .def("addSequence",
            [](IncrementalStatistics& self, const std::vector<Real>& values) {
                self.addSequence(values.begin(), values.end());
            },
            py::arg("values"),
            "Adds a sequence of data to the set.")
        .def("addSequence",
            [](IncrementalStatistics& self, const std::vector<Real>& values,
               const std::vector<Real>& weights) {
                self.addSequence(values.begin(), values.end(),
                                 weights.begin());
            },
            py::arg("values"),
            py::arg("weights"),
            "Adds a sequence of data with weights.")
        .def("reset", &IncrementalStatistics::reset,
            "Resets the data to a null set.");
}
