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
#include <ql/processes/batesprocess.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_processes::batesprocess(py::module_& m) {
    py::class_<BatesProcess, HestonProcess, ext::shared_ptr<BatesProcess>>(
        m, "BatesProcess",
        "Bates stochastic volatility process with jumps.")
        .def(py::init<const Handle<YieldTermStructure>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<Quote>&,
                      Real, Real, Real, Real, Real,
                      Real, Real, Real,
                      HestonProcess::Discretization>(),
            py::arg("riskFreeRate"),
            py::arg("dividendYield"),
            py::arg("s0"),
            py::arg("v0"),
            py::arg("kappa"),
            py::arg("theta"),
            py::arg("sigma"),
            py::arg("rho"),
            py::arg("lambda"),
            py::arg("nu"),
            py::arg("delta"),
            py::arg("discretization") = HestonProcess::FullTruncation,
            "Constructs Bates process with Heston parameters plus jump parameters.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& riskFree,
                         const ext::shared_ptr<YieldTermStructure>& dividend,
                         const ext::shared_ptr<Quote>& spot,
                         Real v0, Real kappa, Real theta, Real sigma, Real rho,
                         Real lambda, Real nu, Real delta,
                         HestonProcess::Discretization d) {
            return ext::make_shared<BatesProcess>(
                Handle<YieldTermStructure>(riskFree),
                Handle<YieldTermStructure>(dividend),
                Handle<Quote>(spot),
                v0, kappa, theta, sigma, rho,
                lambda, nu, delta, d);
        }),
            py::arg("riskFreeRate"),
            py::arg("dividendYield"),
            py::arg("s0"),
            py::arg("v0"),
            py::arg("kappa"),
            py::arg("theta"),
            py::arg("sigma"),
            py::arg("rho"),
            py::arg("lambda"),
            py::arg("nu"),
            py::arg("delta"),
            py::arg("discretization") = HestonProcess::FullTruncation,
            "Constructs with term structures and quote (handles created internally).")
        .def("lambda_", &BatesProcess::lambda, "Returns jump intensity.")
        .def("nu", &BatesProcess::nu, "Returns mean jump size.")
        .def("delta", &BatesProcess::delta, "Returns jump size volatility.");
}
