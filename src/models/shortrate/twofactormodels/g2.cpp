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
#include <ql/models/shortrate/twofactormodels/g2.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/option.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::g2(py::module_& m) {
    py::class_<G2, TwoFactorModel, AffineModel, TermStructureConsistentModel,
               ext::shared_ptr<G2>>(
        m, "G2",
        "Two-additive-factor Gaussian model G2++.")
        // Constructor with handle
        .def(py::init<const Handle<YieldTermStructure>&, Real, Real, Real, Real, Real>(),
            py::arg("termStructure"),
            py::arg("a") = 0.1,
            py::arg("sigma") = 0.01,
            py::arg("b") = 0.1,
            py::arg("eta") = 0.01,
            py::arg("rho") = -0.75,
            "Constructs G2++ model with term structure and parameters.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& ts,
                        Real a, Real sigma, Real b, Real eta, Real rho) {
            return ext::make_shared<G2>(
                Handle<YieldTermStructure>(ts), a, sigma, b, eta, rho);
        }),
            py::arg("termStructure"),
            py::arg("a") = 0.1,
            py::arg("sigma") = 0.01,
            py::arg("b") = 0.1,
            py::arg("eta") = 0.01,
            py::arg("rho") = -0.75,
            "Constructs G2++ model from term structure.")
        // Parameter accessors
        .def("a", &G2::a, "Returns first factor mean reversion speed.")
        .def("sigma", &G2::sigma, "Returns first factor volatility.")
        .def("b", &G2::b, "Returns second factor mean reversion speed.")
        .def("eta", &G2::eta, "Returns second factor volatility.")
        .def("rho", &G2::rho, "Returns correlation between factors.")
        // Pricing methods
        .def("discountBond",
            py::overload_cast<Time, Time, Rate, Rate>(&G2::discountBond, py::const_),
            py::arg("t"), py::arg("T"), py::arg("x"), py::arg("y"),
            "Returns discount bond price P(t,T) given state variables x and y.")
        .def("discountBondOption",
            py::overload_cast<Option::Type, Real, Time, Time>(
                &G2::discountBondOption, py::const_),
            py::arg("type"), py::arg("strike"), py::arg("maturity"), py::arg("bondMaturity"),
            "Returns discount bond option price.");
}
