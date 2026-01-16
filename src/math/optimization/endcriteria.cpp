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
#include <ql/math/optimization/endcriteria.hpp>
#include <pybind11/pybind11.h>
#include <sstream>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::endcriteria(py::module_& m) {
    py::class_<EndCriteria> pyEndCriteria(m, "EndCriteria",
        "Criteria to end optimization processes.");

    py::enum_<EndCriteria::Type>(pyEndCriteria, "Type",
        "End criteria type enumeration.")
        .value("None_", EndCriteria::Type::None)
        .value("MaxIterations", EndCriteria::Type::MaxIterations)
        .value("StationaryPoint", EndCriteria::Type::StationaryPoint)
        .value("StationaryFunctionValue", EndCriteria::Type::StationaryFunctionValue)
        .value("StationaryFunctionAccuracy", EndCriteria::Type::StationaryFunctionAccuracy)
        .value("ZeroGradientNorm", EndCriteria::Type::ZeroGradientNorm)
        .value("FunctionEpsilonTooSmall", EndCriteria::Type::FunctionEpsilonTooSmall)
        .value("Unknown", EndCriteria::Type::Unknown);

    pyEndCriteria
        .def(py::init<Size, Size, Real, Real, Real>(),
            py::arg("maxIterations"),
            py::arg("maxStationaryStateIterations"),
            py::arg("rootEpsilon"),
            py::arg("functionEpsilon"),
            py::arg("gradientNormEpsilon"),
            "Creates end criteria for optimization.")
        .def_property_readonly("maxIterations", &EndCriteria::maxIterations,
            "Returns the maximum number of iterations.")
        .def_property_readonly("maxStationaryStateIterations",
            &EndCriteria::maxStationaryStateIterations,
            "Returns the maximum stationary state iterations.")
        .def_property_readonly("rootEpsilon", &EndCriteria::rootEpsilon,
            "Returns the root epsilon.")
        .def_property_readonly("functionEpsilon", &EndCriteria::functionEpsilon,
            "Returns the function epsilon.")
        .def_property_readonly("gradientNormEpsilon", &EndCriteria::gradientNormEpsilon,
            "Returns the gradient norm epsilon.")
        .def("checkMaxIterations",
            [](const EndCriteria& self, Size iteration, EndCriteria::Type ecType) {
                bool result = self.checkMaxIterations(iteration, ecType);
                return py::make_tuple(result, ecType);
            },
            py::arg("iteration"), py::arg("ecType"),
            "Checks if maximum iterations reached. Returns (bool, ecType).")
        .def("checkStationaryPoint",
            [](const EndCriteria& self, Real xOld, Real xNew,
               Size statState, EndCriteria::Type ecType) {
                bool result = self.checkStationaryPoint(xOld, xNew, statState, ecType);
                return py::make_tuple(result, ecType);
            },
            py::arg("xOld"), py::arg("xNew"),
            py::arg("statState"), py::arg("ecType"),
            "Checks for stationary point. Returns (bool, ecType).")
        .def("checkStationaryFunctionValue",
            [](const EndCriteria& self, Real fxOld, Real fxNew,
               Size statStateIterations, EndCriteria::Type ecType) {
                bool result = self.checkStationaryFunctionValue(fxOld, fxNew,
                    statStateIterations, ecType);
                return py::make_tuple(result, statStateIterations, ecType);
            },
            py::arg("fxOld"), py::arg("fxNew"),
            py::arg("statStateIterations"), py::arg("ecType"),
            "Checks for stationary function value. Returns (bool, statStateIterations, ecType).")
        .def("checkStationaryFunctionAccuracy",
            [](const EndCriteria& self, Real f, bool positiveOptimization,
               EndCriteria::Type ecType) {
                bool result = self.checkStationaryFunctionAccuracy(f,
                    positiveOptimization, ecType);
                return py::make_tuple(result, ecType);
            },
            py::arg("f"), py::arg("positiveOptimization"), py::arg("ecType"),
            "Checks for stationary function accuracy. Returns (bool, ecType).")
        .def("checkZeroGradientNorm",
            [](const EndCriteria& self, Real gNorm, EndCriteria::Type ecType) {
                bool result = self.checkZeroGradientNorm(gNorm, ecType);
                return py::make_tuple(result, ecType);
            },
            py::arg("gNorm"), py::arg("ecType"),
            "Checks for zero gradient norm. Returns (bool, ecType).")
        .def_static("succeeded", &EndCriteria::succeeded,
            py::arg("ecType"),
            "Returns true if the optimization succeeded.");
}
