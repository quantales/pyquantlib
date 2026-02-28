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
#include <ql/processes/hestonslvprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_processes::hestonslvprocess(py::module_& m) {
    py::class_<HestonSLVProcess, StochasticProcess,
               ext::shared_ptr<HestonSLVProcess>>(
        m, "HestonSLVProcess",
        "Heston stochastic local volatility process.")
        .def(py::init<const ext::shared_ptr<HestonProcess>&,
                       ext::shared_ptr<LocalVolTermStructure>,
                       Real>(),
            py::arg("hestonProcess"),
            py::arg("leverageFct"),
            py::arg("mixingFactor") = 1.0,
            "Constructs from Heston process and leverage function.")
        .def("size", &HestonSLVProcess::size,
            "Returns process dimension (2).")
        .def("factors", &HestonSLVProcess::factors,
            "Returns number of Brownian factors (2).")
        .def("v0", &HestonSLVProcess::v0,
            "Returns initial variance.")
        .def("rho", &HestonSLVProcess::rho,
            "Returns correlation.")
        .def("kappa", &HestonSLVProcess::kappa,
            "Returns mean reversion speed.")
        .def("theta", &HestonSLVProcess::theta,
            "Returns long-term variance.")
        .def("sigma", &HestonSLVProcess::sigma,
            "Returns volatility of volatility.")
        .def("mixingFactor", &HestonSLVProcess::mixingFactor,
            "Returns mixing factor.")
        .def("leverageFct", &HestonSLVProcess::leverageFct,
            "Returns leverage function.")
        .def("s0", &HestonSLVProcess::s0,
            py::return_value_policy::reference_internal,
            "Returns spot price handle.")
        .def("dividendYield", &HestonSLVProcess::dividendYield,
            py::return_value_policy::reference_internal,
            "Returns dividend yield handle.")
        .def("riskFreeRate", &HestonSLVProcess::riskFreeRate,
            py::return_value_policy::reference_internal,
            "Returns risk-free rate handle.");
}
