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
#include "pyquantlib/shared_ptr_from_python.h"
#include <ql/termstructures/volatility/kahalesmilesection.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::kahalesmilesection(py::module_& m) {
    py::class_<KahaleSmileSection, SmileSection,
               ext::shared_ptr<KahaleSmileSection>>(
        m, "KahaleSmileSection",
        "Arbitrage-free smile section using Kahale's C^1 inter- and "
        "extrapolation method.")
        .def(py::init([](const py::object& sourceObj,
                         const py::object& atm,
                         bool interpolate,
                         bool exponentialExtrapolation,
                         bool deleteArbitragePoints,
                         const std::vector<Real>& moneynessGrid,
                         Real gap,
                         int forcedLeftIndex,
                         int forcedRightIndex) {
                auto source = shared_ptr_from_python<SmileSection>(sourceObj);
                Real atmVal = atm.is_none() ? Null<Real>() : atm.cast<Real>();
                return ext::make_shared<KahaleSmileSection>(
                    source, atmVal, interpolate, exponentialExtrapolation,
                    deleteArbitragePoints, moneynessGrid, gap,
                    forcedLeftIndex, forcedRightIndex);
            }),
            py::arg("source"),
            py::arg("atm") = py::none(),
            py::arg("interpolate") = false,
            py::arg("exponentialExtrapolation") = false,
            py::arg("deleteArbitragePoints") = false,
            py::arg("moneynessGrid") = std::vector<Real>(),
            py::arg("gap") = 1.0E-5,
            py::arg("forcedLeftIndex") = -1,
            py::arg("forcedRightIndex") = QL_MAX_INTEGER,
            "Constructs from a source SmileSection, optionally specifying "
            "ATM level, interpolation, and extrapolation parameters.")
        .def("leftCoreStrike", &KahaleSmileSection::leftCoreStrike,
            "Returns the leftmost core region strike.")
        .def("rightCoreStrike", &KahaleSmileSection::rightCoreStrike,
            "Returns the rightmost core region strike.")
        .def("coreIndices", &KahaleSmileSection::coreIndices,
            "Returns (left, right) indices of the core region.");
}
