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
#include <ql/termstructures/volatility/sabrinterpolatedsmilesection.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::sabrinterpolatedsmilesection(py::module_& m) {
    py::classh<SabrInterpolatedSmileSection, SmileSection, LazyObject>(
        m, "SabrInterpolatedSmileSection",
        "Smile section calibrated via SABR interpolation.")
        .def(py::init<const Date&, Rate, const std::vector<Rate>&,
                      bool, Volatility, const std::vector<Volatility>&,
                      Real, Real, Real, Real,
                      bool, bool, bool, bool, bool,
                      const ext::shared_ptr<EndCriteria>&,
                      const ext::shared_ptr<OptimizationMethod>&,
                      const DayCounter&, Real>(),
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
            py::arg("shift") = 0.0,
            "Constructs and calibrates SABR to market strikes and volatilities.")
        .def("alpha", &SabrInterpolatedSmileSection::alpha,
            "Returns calibrated SABR alpha.")
        .def("beta", &SabrInterpolatedSmileSection::beta,
            "Returns calibrated SABR beta.")
        .def("nu", &SabrInterpolatedSmileSection::nu,
            "Returns calibrated SABR nu.")
        .def("rho", &SabrInterpolatedSmileSection::rho,
            "Returns calibrated SABR rho.")
        .def("rmsError", &SabrInterpolatedSmileSection::rmsError,
            "Returns RMS calibration error.")
        .def("maxError", &SabrInterpolatedSmileSection::maxError,
            "Returns maximum calibration error.")
        .def("endCriteria", &SabrInterpolatedSmileSection::endCriteria,
            "Returns end criteria type from calibration.");
}
