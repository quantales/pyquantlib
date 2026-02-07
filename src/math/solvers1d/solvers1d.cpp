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
#include <ql/math/solvers1d/brent.hpp>
#include <ql/math/solvers1d/bisection.hpp>
#include <ql/math/solvers1d/secant.hpp>
#include <ql/math/solvers1d/newton.hpp>
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

} // anonymous namespace

void ql_math::solvers1d(py::module_& m) {
    auto brent = py::class_<Brent>(m, "Brent", "Brent 1-D solver.");
    bindSolverMethods(brent);

    auto bisection = py::class_<Bisection>(
        m, "Bisection", "Bisection 1-D solver.");
    bindSolverMethods(bisection);

    auto secant = py::class_<Secant>(m, "Secant", "Secant 1-D solver.");
    bindSolverMethods(secant);

    py::class_<Newton>(m, "Newton",
        "Newton 1-D solver (requires derivative function).")
        .def(py::init<>())
        .def("solve",
            [](Newton& s, py::function f, py::function df,
               Real accuracy, Real guess, Real step) {
                return s.solve(PyFuncWithDerivative{f, df},
                               accuracy, guess, step);
            },
            py::arg("f"), py::arg("derivative"), py::arg("accuracy"),
            py::arg("guess"), py::arg("step"),
            "Finds root with automatic bracketing.")
        .def("solve",
            [](Newton& s, py::function f, py::function df,
               Real accuracy, Real guess, Real xMin, Real xMax) {
                return s.solve(PyFuncWithDerivative{f, df},
                               accuracy, guess, xMin, xMax);
            },
            py::arg("f"), py::arg("derivative"), py::arg("accuracy"),
            py::arg("guess"), py::arg("xMin"), py::arg("xMax"),
            "Finds root within explicit bracket.")
        .def("setMaxEvaluations", &Solver1D<Newton>::setMaxEvaluations,
            py::arg("evaluations"),
            "Sets maximum number of function evaluations.")
        .def("setLowerBound", &Solver1D<Newton>::setLowerBound,
            py::arg("lowerBound"),
            "Sets lower bound for the function domain.")
        .def("setUpperBound", &Solver1D<Newton>::setUpperBound,
            py::arg("upperBound"),
            "Sets upper bound for the function domain.");
}
