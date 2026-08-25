/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/methods/finitedifferences/utilities/smilesectionrndcalculator.hpp>
#include <ql/termstructures/volatility/smilesection.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::smilesectionrndcalculator(py::module_& m) {
    py::class_<SmileSectionRNDCalculator,
               ext::shared_ptr<SmileSectionRNDCalculator>,
               RiskNeutralDensityCalculator>(
        m, "SmileSectionRNDCalculator",
        "Risk-neutral density implied by a smile section.")
        .def(py::init<ext::shared_ptr<SmileSection>, Size, Real>(),
            py::arg("smile"),
            py::arg("nStrikes") = 200,
            py::arg("nStd") = 5.0,
            "Constructs from a smile section, sampling nStrikes points over "
            "nStd standard deviations.")
        .def("pdf",
            py::overload_cast<Real, Time>(&SmileSectionRNDCalculator::pdf, py::const_),
            py::arg("x"), py::arg("t"),
            "Returns the density at x = ln(S) and time t, which must match the "
            "smile's exercise time.")
        .def("cdf",
            py::overload_cast<Real, Time>(&SmileSectionRNDCalculator::cdf, py::const_),
            py::arg("x"), py::arg("t"),
            "Returns the cumulative probability at x = ln(S) and time t.")
        .def("invcdf",
            py::overload_cast<Real, Time>(&SmileSectionRNDCalculator::invcdf, py::const_),
            py::arg("p"), py::arg("t"),
            "Returns the quantile x = ln(S) for probability p at time t.")
        .def("pdf",
            py::overload_cast<Real>(&SmileSectionRNDCalculator::pdf, py::const_),
            py::arg("x"),
            "Returns the density at x = ln(S) at the smile's exercise time.")
        .def("cdf",
            py::overload_cast<Real>(&SmileSectionRNDCalculator::cdf, py::const_),
            py::arg("x"),
            "Returns the cumulative probability at x = ln(S) at the smile's "
            "exercise time.")
        .def("invcdf",
            py::overload_cast<Real>(&SmileSectionRNDCalculator::invcdf, py::const_),
            py::arg("p"),
            "Returns the quantile x = ln(S) for probability p at the smile's "
            "exercise time.");
}
