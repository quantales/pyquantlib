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
#include <ql/models/shortrate/onefactormodels/hullwhite.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/option.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::hullwhite(py::module_& m) {
    // HullWhite model
    // NOTE: TermStructureConsistentModel is NOT specified as a base to avoid
    // pybind11 diamond inheritance issues. The termStructure() method is bound directly.
    py::class_<HullWhite, Vasicek, ext::shared_ptr<HullWhite>>(
        m, "HullWhite",
        "Hull-White extended Vasicek model: dr = (theta(t) - a*r)dt + sigma*dW.")
        // Constructor with handle
        .def(py::init<const Handle<YieldTermStructure>&, Real, Real>(),
            py::arg("termStructure"),
            py::arg("a") = 0.1,
            py::arg("sigma") = 0.01,
            "Constructs Hull-White model with term structure, mean reversion, and volatility.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& ts,
                        Real a, Real sigma) {
            return ext::make_shared<HullWhite>(
                Handle<YieldTermStructure>(ts), a, sigma);
        }),
            py::arg("termStructure"),
            py::arg("a") = 0.1,
            py::arg("sigma") = 0.01,
            "Constructs Hull-White model from term structure.")
        // From TermStructureConsistentModel (bound directly)
        .def("termStructure", &HullWhite::termStructure,
            "Returns the term structure handle.")
        // Methods
        .def("discountBondOption",
            py::overload_cast<Option::Type, Real, Time, Time>(
                &HullWhite::discountBondOption, py::const_),
            py::arg("type"), py::arg("strike"), py::arg("maturity"), py::arg("bondMaturity"),
            "Returns discount bond option price.")
        .def_static("convexityBias", &HullWhite::convexityBias,
            py::arg("futurePrice"), py::arg("t"), py::arg("T"),
            py::arg("sigma"), py::arg("a"),
            "Computes futures convexity bias.");
}
