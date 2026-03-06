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
#include <ql/experimental/volatility/noarbsabrinterpolatedsmilesection.hpp>
#include <ql/math/optimization/endcriteria.hpp>
#include <ql/math/optimization/method.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::noarbsabrinterpolatedsmilesection(py::module_& m) {
    py::class_<NoArbSabrInterpolatedSmileSection, SmileSection,
               ext::shared_ptr<NoArbSabrInterpolatedSmileSection>>(
        m, "NoArbSabrInterpolatedSmileSection",
        "Smile section calibrated to market data using no-arbitrage SABR "
        "interpolation. Inherits from both SmileSection and LazyObject.")
        // No-quotes constructor (most common usage)
        .def(py::init([](const Date& optionDate,
                         Rate forward,
                         const std::vector<Rate>& strikes,
                         bool hasFloatingStrikes,
                         Volatility atmVolatility,
                         const std::vector<Volatility>& vols,
                         Real alpha, Real beta, Real nu, Real rho,
                         bool isAlphaFixed, bool isBetaFixed,
                         bool isNuFixed, bool isRhoFixed,
                         bool vegaWeighted,
                         const ext::shared_ptr<EndCriteria>& endCriteria,
                         const ext::shared_ptr<OptimizationMethod>& method,
                         const DayCounter& dc) {
                return ext::make_shared<NoArbSabrInterpolatedSmileSection>(
                    optionDate, forward, strikes, hasFloatingStrikes,
                    atmVolatility, vols, alpha, beta, nu, rho,
                    isAlphaFixed, isBetaFixed, isNuFixed, isRhoFixed,
                    vegaWeighted, endCriteria, method, dc);
            }),
            py::arg("optionDate"),
            py::arg("forward"),
            py::arg("strikes"),
            py::arg("hasFloatingStrikes"),
            py::arg("atmVolatility"),
            py::arg("vols"),
            py::arg("alpha"), py::arg("beta"),
            py::arg("nu"), py::arg("rho"),
            py::arg("isAlphaFixed") = false,
            py::arg("isBetaFixed") = false,
            py::arg("isNuFixed") = false,
            py::arg("isRhoFixed") = false,
            py::arg("vegaWeighted") = true,
            py::arg("endCriteria") = ext::shared_ptr<EndCriteria>(),
            py::arg("method") = ext::shared_ptr<OptimizationMethod>(),
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs from market data (no quotes).")
        .def("alpha", &NoArbSabrInterpolatedSmileSection::alpha)
        .def("beta", &NoArbSabrInterpolatedSmileSection::beta)
        .def("nu", &NoArbSabrInterpolatedSmileSection::nu)
        .def("rho", &NoArbSabrInterpolatedSmileSection::rho)
        .def("rmsError", &NoArbSabrInterpolatedSmileSection::rmsError,
            "Returns RMS calibration error.")
        .def("maxError", &NoArbSabrInterpolatedSmileSection::maxError,
            "Returns maximum calibration error.")
        .def("endCriteria", &NoArbSabrInterpolatedSmileSection::endCriteria,
            "Returns end criteria type after calibration.");
}
