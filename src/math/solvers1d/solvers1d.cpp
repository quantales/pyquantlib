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
#include <ql/math/solvers1d/brent.hpp>
#include <ql/math/solvers1d/bisection.hpp>
#include <ql/math/solvers1d/secant.hpp>
#include <ql/math/solvers1d/newton.hpp>
#include <ql/math/solvers1d/newtonsafe.hpp>
#include <ql/math/solvers1d/halley.hpp>
#include <ql/math/solvers1d/falseposition.hpp>
#include <ql/math/solvers1d/ridder.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>

namespace py = pybind11;
using namespace QuantLib;

namespace {

    // Wraps a Python callable for QuantLib solvers
    struct PyFunc {
        py::function f;
        Real operator()(Real x) const { return f(x).cast<Real>(); }
    };

    // Wraps a Python callable with separate derivative for Newton solver
    struct PyFuncWithDerivative {
        py::function f;
        py::function df;
        Real operator()(Real x) const { return f(x).cast<Real>(); }
        Real derivative(Real x) const { return df(x).cast<Real>(); }
    };

    // Wraps a Python callable with first and second derivatives for Halley solver
    struct PyFuncWithSecondDerivative {
        py::function f;
        py::function df;
        py::function d2f;
        Real operator()(Real x) const { return f(x).cast<Real>(); }
        Real derivative(Real x) const { return df(x).cast<Real>(); }
        Real secondDerivative(Real x) const { return d2f(x).cast<Real>(); }
    };

    // Binds common solver methods (solve overloads, setMaxEvaluations, bounds)
    template <typename Solver>
    void bindSolverMethods(py::class_<Solver>& cls) {
        using Base = Solver1D<Solver>;
        cls.def(py::init<>())
            .def("solve",
                [](Solver& s, py::function f, Real accuracy,
                   Real guess, Real step) {
                    return s.solve(PyFunc{f}, accuracy, guess, step);
                },
                py::arg("f"), py::arg("accuracy"),
                py::arg("guess"), py::arg("step"),
                "Finds root with automatic bracketing.")
            .def("solve",
                [](Solver& s, py::function f, Real accuracy,
                   Real guess, Real xMin, Real xMax) {
                    return s.solve(PyFunc{f}, accuracy, guess, xMin, xMax);
                },
                py::arg("f"), py::arg("accuracy"),
                py::arg("guess"), py::arg("xMin"), py::arg("xMax"),
                "Finds root within explicit bracket.")
            .def("setMaxEvaluations", &Base::setMaxEvaluations,
                py::arg("evaluations"),
                "Sets maximum number of function evaluations.")
            .def("setLowerBound", &Base::setLowerBound,
                py::arg("lowerBound"),
                "Sets lower bound for the function domain.")
            .def("setUpperBound", &Base::setUpperBound,
                py::arg("upperBound"),
                "Sets upper bound for the function domain.");
    }

    // Binds a solver whose objective also supplies a first derivative
    template <typename Solver>
    void bindDerivativeSolver(py::module_& m, const char* name, const char* doc) {
        using Base = Solver1D<Solver>;
        py::class_<Solver>(m, name, doc)
            .def(py::init<>())
            .def("solve",
                [](Solver& s, py::function f, py::function df,
                   Real accuracy, Real guess, Real step) {
                    return s.solve(PyFuncWithDerivative{f, df},
                                   accuracy, guess, step);
                },
                py::arg("f"), py::arg("derivative"), py::arg("accuracy"),
                py::arg("guess"), py::arg("step"),
                "Finds root with automatic bracketing.")
            .def("solve",
                [](Solver& s, py::function f, py::function df,
                   Real accuracy, Real guess, Real xMin, Real xMax) {
                    return s.solve(PyFuncWithDerivative{f, df},
                                   accuracy, guess, xMin, xMax);
                },
                py::arg("f"), py::arg("derivative"), py::arg("accuracy"),
                py::arg("guess"), py::arg("xMin"), py::arg("xMax"),
                "Finds root within explicit bracket.")
            .def("setMaxEvaluations", &Base::setMaxEvaluations,
                py::arg("evaluations"),
                "Sets maximum number of function evaluations.")
            .def("setLowerBound", &Base::setLowerBound,
                py::arg("lowerBound"),
                "Sets lower bound for the function domain.")
            .def("setUpperBound", &Base::setUpperBound,
                py::arg("upperBound"),
                "Sets upper bound for the function domain.");
    }

} // anonymous namespace

void ql_math::solvers1d(py::module_& m) {
    auto brent = py::class_<Brent>(m, "Brent", "Brent 1-D solver.");
    bindSolverMethods(brent);

    auto bisection = py::class_<Bisection>(
        m, "Bisection", "Bisection 1-D solver.");
    bindSolverMethods(bisection);

    auto secant = py::class_<Secant>(m, "Secant", "Secant 1-D solver.");
    bindSolverMethods(secant);

    bindDerivativeSolver<Newton>(
        m, "Newton", "Newton 1-D solver (requires derivative function).");

    bindDerivativeSolver<NewtonSafe>(
        m, "NewtonSafe",
        "Safe Newton 1-D solver (requires derivative function), falling back "
        "to bisection when a Newton step leaves the bracket.");

    auto falsePosition = py::class_<FalsePosition>(
        m, "FalsePosition", "False position 1-D solver.");
    bindSolverMethods(falsePosition);

    auto ridder = py::class_<Ridder>(m, "Ridder", "Ridder 1-D solver.");
    bindSolverMethods(ridder);

    py::class_<Halley>(m, "Halley",
        "Halley 1-D solver (requires first and second derivative functions).")
        .def(py::init<>())
        .def("solve",
            [](Halley& s, py::function f, py::function df, py::function d2f,
               Real accuracy, Real guess, Real step) {
                return s.solve(PyFuncWithSecondDerivative{f, df, d2f},
                               accuracy, guess, step);
            },
            py::arg("f"), py::arg("derivative"), py::arg("secondDerivative"),
            py::arg("accuracy"), py::arg("guess"), py::arg("step"),
            "Finds root with automatic bracketing.")
        .def("solve",
            [](Halley& s, py::function f, py::function df, py::function d2f,
               Real accuracy, Real guess, Real xMin, Real xMax) {
                return s.solve(PyFuncWithSecondDerivative{f, df, d2f},
                               accuracy, guess, xMin, xMax);
            },
            py::arg("f"), py::arg("derivative"), py::arg("secondDerivative"),
            py::arg("accuracy"), py::arg("guess"), py::arg("xMin"), py::arg("xMax"),
            "Finds root within explicit bracket.")
        .def("setMaxEvaluations", &Solver1D<Halley>::setMaxEvaluations,
            py::arg("evaluations"),
            "Sets maximum number of function evaluations.")
        .def("setLowerBound", &Solver1D<Halley>::setLowerBound,
            py::arg("lowerBound"),
            "Sets lower bound for the function domain.")
        .def("setUpperBound", &Solver1D<Halley>::setUpperBound,
            py::arg("upperBound"),
            "Sets upper bound for the function domain.");
}
