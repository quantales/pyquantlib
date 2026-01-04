/*
 * PyQuantLib: Python bindings for QuantLib
 * Copyright (c) 2025 Yassine Idyiahia
 *
 * QuantLib is Copyright (c) 2000-2025 The QuantLib Authors
 * QuantLib is free software under a modified BSD license.
 * See http://quantlib.org/ for more information.
 *
 * Source: https://github.com/quantales/pyquantlib
 * Licensed under the BSD 3-Clause License. See LICENSE file for details.
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/processes/stochasticprocessarray.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_processes::stochasticprocessarray(py::module_& m) {

    // StochasticProcessArray - array of correlated 1D processes
    py::class_<StochasticProcessArray, ext::shared_ptr<StochasticProcessArray>, StochasticProcess>(
        m, "StochasticProcessArray", "Array of correlated 1-D stochastic processes.")
        .def(py::init<const std::vector<ext::shared_ptr<StochasticProcess1D>>&, const Matrix&>(),
            py::arg("processes"), py::arg("correlation"),
            "Constructs from a list of 1D processes and correlation matrix.")
        .def("size", &StochasticProcessArray::size,
            "Returns the number of processes.")
        .def("process", &StochasticProcessArray::process,
            py::arg("i"),
            "Returns the i-th process.")
        .def("initialValues", &StochasticProcessArray::initialValues,
            "Returns the initial values of all processes.")
        .def("drift",
            [](const StochasticProcessArray& p, Time t, const Array& x) {
                return p.drift(t, x);
            },
            py::arg("t"), py::arg("x"),
            "Returns the drift at time t and state x.")
        .def("diffusion",
            [](const StochasticProcessArray& p, Time t, const Array& x) {
                return p.diffusion(t, x);
            },
            py::arg("t"), py::arg("x"),
            "Returns the diffusion matrix at time t and state x.")
        .def("expectation",
            [](const StochasticProcessArray& p, Time t0, const Array& x0, Time dt) {
                return p.expectation(t0, x0, dt);
            },
            py::arg("t0"), py::arg("x0"), py::arg("dt"),
            "Returns the expectation of the process.")
        .def("stdDeviation",
            [](const StochasticProcessArray& p, Time t0, const Array& x0, Time dt) {
                return p.stdDeviation(t0, x0, dt);
            },
            py::arg("t0"), py::arg("x0"), py::arg("dt"),
            "Returns the standard deviation matrix.")
        .def("covariance",
            [](const StochasticProcessArray& p, Time t0, const Array& x0, Time dt) {
                return p.covariance(t0, x0, dt);
            },
            py::arg("t0"), py::arg("x0"), py::arg("dt"),
            "Returns the covariance matrix.")
        .def("evolve",
            [](const StochasticProcessArray& p, Time t0, const Array& x0, Time dt, const Array& dw) {
                return p.evolve(t0, x0, dt, dw);
            },
            py::arg("t0"), py::arg("x0"), py::arg("dt"), py::arg("dw"),
            "Returns the asset value after a time interval.")
        .def("correlation", &StochasticProcessArray::correlation,
            "Returns the correlation matrix.");
}
