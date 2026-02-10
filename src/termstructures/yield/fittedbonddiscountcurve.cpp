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
#include <ql/termstructures/yield/fittedbonddiscountcurve.hpp>
#include <ql/termstructures/yield/bondhelpers.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

using FittingMethod = FittedBondDiscountCurve::FittingMethod;

void ql_termstructures::fittingmethod(py::module_& m) {
    py::class_<FittingMethod, ext::shared_ptr<FittingMethod>>(m, "FittingMethod",
        "ABC for bond discount curve fitting methods.")
        // No constructors (protected)
        .def("size", &FittingMethod::size,
            "Returns the number of fitting parameters.")
        .def("solution", &FittingMethod::solution,
            "Returns the fitted parameters.")
        .def("numberOfIterations", &FittingMethod::numberOfIterations,
            "Returns the number of optimization iterations.")
        .def("minimumCostValue", &FittingMethod::minimumCostValue,
            "Returns the minimum cost function value.")
        .def("errorCode", &FittingMethod::errorCode,
            "Returns the optimization error code.")
        .def("constrainAtZero", &FittingMethod::constrainAtZero,
            "Returns whether the curve is constrained at zero.")
        .def("weights", &FittingMethod::weights,
            "Returns the fitting weights.")
        .def("l2", &FittingMethod::l2,
            "Returns the L2 regularization array.")
        .def("optimizationMethod", &FittingMethod::optimizationMethod,
            "Returns the optimization method.")
        .def("discount", &FittingMethod::discount,
            py::arg("x"), py::arg("t"),
            "Returns the discount factor for given parameters and time.");
}

void ql_termstructures::fittedbonddiscountcurve(py::module_& m) {
    // Diamond: YieldTermStructure + LazyObject (both through Observable)
    py::classh<FittedBondDiscountCurve, YieldTermStructure, LazyObject>(
        m, "FittedBondDiscountCurve",
        "Discount curve fitted to a set of bonds.")
        // Settlement days + fitting
        .def(py::init<Natural, const Calendar&,
                      std::vector<ext::shared_ptr<BondHelper>>,
                      const DayCounter&, const FittingMethod&,
                      Real, Size, Array, Real, Size>(),
            py::arg("settlementDays"), py::arg("calendar"),
            py::arg("bonds"), py::arg("dayCounter"),
            py::arg("fittingMethod"),
            py::arg("accuracy") = 1.0e-10,
            py::arg("maxEvaluations") = 10000,
            py::arg("guess") = Array(),
            py::arg("simplexLambda") = 1.0,
            py::arg("maxStationaryStateIterations") = 100,
            "Constructs from settlement days with bond fitting.")
        // Reference date + fitting
        .def(py::init<const Date&,
                      std::vector<ext::shared_ptr<BondHelper>>,
                      const DayCounter&, const FittingMethod&,
                      Real, Size, Array, Real, Size>(),
            py::arg("referenceDate"),
            py::arg("bonds"), py::arg("dayCounter"),
            py::arg("fittingMethod"),
            py::arg("accuracy") = 1.0e-10,
            py::arg("maxEvaluations") = 10000,
            py::arg("guess") = Array(),
            py::arg("simplexLambda") = 1.0,
            py::arg("maxStationaryStateIterations") = 100,
            "Constructs from reference date with bond fitting.")
        // Settlement days + precalculated parameters
        .def(py::init<Natural, const Calendar&,
                      const FittingMethod&, Array, Date, const DayCounter&>(),
            py::arg("settlementDays"), py::arg("calendar"),
            py::arg("fittingMethod"), py::arg("parameters"),
            py::arg("maxDate"), py::arg("dayCounter"),
            "Constructs from settlement days with precalculated parameters.")
        // Reference date + precalculated parameters
        .def(py::init<const Date&,
                      const FittingMethod&, Array, Date, const DayCounter&>(),
            py::arg("referenceDate"),
            py::arg("fittingMethod"), py::arg("parameters"),
            py::arg("maxDate"), py::arg("dayCounter"),
            "Constructs from reference date with precalculated parameters.")
        .def("numberOfBonds", &FittedBondDiscountCurve::numberOfBonds,
            "Returns the number of bonds used in the fit.")
        .def("fitResults", &FittedBondDiscountCurve::fitResults,
            py::return_value_policy::reference_internal,
            "Returns the fitting method with calibration results.")
        .def("resetGuess", &FittedBondDiscountCurve::resetGuess,
            py::arg("guess"),
            "Resets the initial guess for refitting.");
}
