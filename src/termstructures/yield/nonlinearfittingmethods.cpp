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
#include <ql/termstructures/yield/nonlinearfittingmethods.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

using FittingMethod = FittedBondDiscountCurve::FittingMethod;

void ql_termstructures::nonlinearfittingmethods(py::module_& m) {
    // NelsonSiegelFitting
    py::class_<NelsonSiegelFitting, FittingMethod,
               ext::shared_ptr<NelsonSiegelFitting>>(m, "NelsonSiegelFitting",
        "Nelson-Siegel fitting method.")
        .def(py::init<const Array&,
                      const ext::shared_ptr<OptimizationMethod>&,
                      const Array&, Real, Real, Constraint>(),
            py::arg("weights") = Array(),
            py::arg("optimizationMethod") = ext::shared_ptr<OptimizationMethod>(),
            py::arg("l2") = Array(),
            py::arg("minCutoffTime") = 0.0,
            py::arg("maxCutoffTime") = QL_MAX_REAL,
            py::arg("constraint") = NoConstraint(),
            "Constructs a Nelson-Siegel fitting method.");

    // SvenssonFitting
    py::class_<SvenssonFitting, FittingMethod,
               ext::shared_ptr<SvenssonFitting>>(m, "SvenssonFitting",
        "Svensson fitting method.")
        .def(py::init<const Array&,
                      const ext::shared_ptr<OptimizationMethod>&,
                      const Array&, Real, Real, Constraint>(),
            py::arg("weights") = Array(),
            py::arg("optimizationMethod") = ext::shared_ptr<OptimizationMethod>(),
            py::arg("l2") = Array(),
            py::arg("minCutoffTime") = 0.0,
            py::arg("maxCutoffTime") = QL_MAX_REAL,
            py::arg("constraint") = NoConstraint(),
            "Constructs a Svensson fitting method.");

    // ExponentialSplinesFitting
    py::class_<ExponentialSplinesFitting, FittingMethod,
               ext::shared_ptr<ExponentialSplinesFitting>>(
        m, "ExponentialSplinesFitting",
        "Exponential splines fitting method.")
        .def(py::init([](bool constrainAtZero,
                         const Array& weights,
                         const ext::shared_ptr<OptimizationMethod>& optimizationMethod,
                         const Array& l2,
                         Real minCutoffTime, Real maxCutoffTime,
                         Size numCoeffs,
                         const py::object& fixedKappa,
                         Constraint constraint) {
            Real kappa = Null<Real>();
            if (!fixedKappa.is_none())
                kappa = fixedKappa.cast<Real>();
            return ExponentialSplinesFitting(
                constrainAtZero, weights, optimizationMethod, l2,
                minCutoffTime, maxCutoffTime, numCoeffs, kappa, constraint);
        }),
            py::arg("constrainAtZero") = true,
            py::arg("weights") = Array(),
            py::arg("optimizationMethod") = ext::shared_ptr<OptimizationMethod>(),
            py::arg("l2") = Array(),
            py::arg("minCutoffTime") = 0.0,
            py::arg("maxCutoffTime") = QL_MAX_REAL,
            py::arg("numCoeffs") = 9,
            py::arg("fixedKappa") = py::none(),
            py::arg("constraint") = NoConstraint(),
            "Constructs an exponential splines fitting method.");

    // CubicBSplinesFitting
    py::class_<CubicBSplinesFitting, FittingMethod,
               ext::shared_ptr<CubicBSplinesFitting>>(m, "CubicBSplinesFitting",
        "Cubic B-splines fitting method.")
        .def(py::init<const std::vector<Time>&, bool,
                      const Array&,
                      const ext::shared_ptr<OptimizationMethod>&,
                      const Array&, Real, Real, Constraint>(),
            py::arg("knotVector"),
            py::arg("constrainAtZero") = true,
            py::arg("weights") = Array(),
            py::arg("optimizationMethod") = ext::shared_ptr<OptimizationMethod>(),
            py::arg("l2") = Array(),
            py::arg("minCutoffTime") = 0.0,
            py::arg("maxCutoffTime") = QL_MAX_REAL,
            py::arg("constraint") = NoConstraint(),
            "Constructs a cubic B-splines fitting method.")
        .def("basisFunction", &CubicBSplinesFitting::basisFunction,
            py::arg("i"), py::arg("t"),
            "Returns the i-th basis function value at time t.");

    // SimplePolynomialFitting
    py::class_<SimplePolynomialFitting, FittingMethod,
               ext::shared_ptr<SimplePolynomialFitting>>(
        m, "SimplePolynomialFitting",
        "Simple polynomial fitting method.")
        .def(py::init<Natural, bool,
                      const Array&,
                      const ext::shared_ptr<OptimizationMethod>&,
                      const Array&, Real, Real, Constraint>(),
            py::arg("degree"),
            py::arg("constrainAtZero") = true,
            py::arg("weights") = Array(),
            py::arg("optimizationMethod") = ext::shared_ptr<OptimizationMethod>(),
            py::arg("l2") = Array(),
            py::arg("minCutoffTime") = 0.0,
            py::arg("maxCutoffTime") = QL_MAX_REAL,
            py::arg("constraint") = NoConstraint(),
            "Constructs a simple polynomial fitting method.");

    // SpreadFittingMethod
    py::class_<SpreadFittingMethod, FittingMethod,
               ext::shared_ptr<SpreadFittingMethod>>(m, "SpreadFittingMethod",
        "Spread fitting method over a reference curve.")
        // Explicit handle
        .def(py::init<const ext::shared_ptr<FittingMethod>&,
                      Handle<YieldTermStructure>,
                      Real, Real>(),
            py::arg("method"), py::arg("discountCurve"),
            py::arg("minCutoffTime") = 0.0,
            py::arg("maxCutoffTime") = QL_MAX_REAL,
            "Constructs with a discount curve handle.")
        // Hidden handle
        .def(py::init([](const ext::shared_ptr<FittingMethod>& method,
                         const py::object& discountCurve,
                         Real minCutoffTime, Real maxCutoffTime) {
            return SpreadFittingMethod(
                method,
                Handle<YieldTermStructure>(
                    shared_ptr_from_python<YieldTermStructure>(discountCurve)),
                minCutoffTime, maxCutoffTime);
        }),
            py::arg("method"), py::arg("discountCurve"),
            py::arg("minCutoffTime") = 0.0,
            py::arg("maxCutoffTime") = QL_MAX_REAL,
            "Constructs with a discount curve (handle created internally).");
}
