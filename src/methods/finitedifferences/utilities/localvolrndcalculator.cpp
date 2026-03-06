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
#include <ql/methods/finitedifferences/utilities/localvolrndcalculator.hpp>
#include <ql/termstructures/volatility/equityfx/localvoltermstructure.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/quote.hpp>
#include <ql/timegrid.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::localvolrndcalculator(py::module_& m) {
    py::class_<LocalVolRNDCalculator,
               ext::shared_ptr<LocalVolRNDCalculator>,
               RiskNeutralDensityCalculator>(
        m, "LocalVolRNDCalculator",
        "Risk-neutral density calculator using local volatility and FDM.")
        .def(py::init([](const ext::shared_ptr<Quote>& spot,
                         const ext::shared_ptr<YieldTermStructure>& rTS,
                         const ext::shared_ptr<YieldTermStructure>& qTS,
                         const ext::shared_ptr<LocalVolTermStructure>& localVol,
                         Size xGrid, Size tGrid,
                         Real x0Density, Real localVolProbEps,
                         Size maxIter,
                         const py::object& gaussianStepSize) {
            Time gss = gaussianStepSize.is_none()
                ? -Null<Time>()
                : gaussianStepSize.cast<Time>();
            return ext::make_shared<LocalVolRNDCalculator>(
                spot, rTS, qTS, localVol,
                xGrid, tGrid, x0Density, localVolProbEps, maxIter, gss);
        }),
            py::arg("spot"), py::arg("rTS"), py::arg("qTS"),
            py::arg("localVol"),
            py::arg("xGrid") = 101, py::arg("tGrid") = 51,
            py::arg("x0Density") = 0.1, py::arg("localVolProbEps") = 1e-6,
            py::arg("maxIter") = 10000,
            py::arg("gaussianStepSize") = py::none(),
            "Constructs from spot, yield curves, local vol surface, and grid parameters.")
        .def(py::init([](const ext::shared_ptr<Quote>& spot,
                         const ext::shared_ptr<YieldTermStructure>& rTS,
                         const ext::shared_ptr<YieldTermStructure>& qTS,
                         const ext::shared_ptr<LocalVolTermStructure>& localVol,
                         const ext::shared_ptr<TimeGrid>& timeGrid,
                         Size xGrid,
                         Real x0Density, Real eps,
                         Size maxIter,
                         const py::object& gaussianStepSize) {
            Time gss = gaussianStepSize.is_none()
                ? -Null<Time>()
                : gaussianStepSize.cast<Time>();
            return ext::make_shared<LocalVolRNDCalculator>(
                spot, rTS, qTS, localVol, timeGrid,
                xGrid, x0Density, eps, maxIter, gss);
        }),
            py::arg("spot"), py::arg("rTS"), py::arg("qTS"),
            py::arg("localVol"), py::arg("timeGrid"),
            py::arg("xGrid") = 101,
            py::arg("x0Density") = 0.1, py::arg("eps") = 1e-6,
            py::arg("maxIter") = 10000,
            py::arg("gaussianStepSize") = py::none(),
            "Constructs from spot, yield curves, local vol, and explicit time grid.")
        .def("pdf", &LocalVolRNDCalculator::pdf,
            py::arg("x"), py::arg("t"),
            "Returns the probability density at x and time t.")
        .def("cdf", &LocalVolRNDCalculator::cdf,
            py::arg("x"), py::arg("t"),
            "Returns the cumulative distribution at x and time t.")
        .def("invcdf", &LocalVolRNDCalculator::invcdf,
            py::arg("p"), py::arg("t"),
            "Returns the inverse CDF at probability p and time t.")
        .def("timeGrid", &LocalVolRNDCalculator::timeGrid,
            "Returns the time grid.")
        .def("mesher", &LocalVolRNDCalculator::mesher,
            py::arg("t"),
            "Returns the 1D mesher at time t.");
}
