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
#include "pyquantlib/trampolines.h"
#include <ql/stochasticprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_core::stochasticprocess(py::module_& m) {
    py::module_ base = m.def_submodule("base", "Abstract base classes");

    // StochasticProcess ABC
    py::class_<StochasticProcess, PyStochasticProcess, ext::shared_ptr<StochasticProcess>,
               Observer, Observable>(base, "StochasticProcess",
        "Abstract base class for stochastic processes.")
        .def(py::init_alias<>())
        .def("size", &StochasticProcess::size,
            "Returns the number of dimensions.")
        .def("factors", &StochasticProcess::factors,
            "Returns the number of Brownian factors.")
        .def("initialValues", &StochasticProcess::initialValues,
            "Returns the initial values.")
        .def("drift", &StochasticProcess::drift,
            py::arg("t"), py::arg("x"),
            "Returns the drift at time t given state x.")
        .def("diffusion", &StochasticProcess::diffusion,
            py::arg("t"), py::arg("x"),
            "Returns the diffusion matrix at time t given state x.")
        .def("evolve", &StochasticProcess::evolve,
            py::arg("t0"), py::arg("x0"), py::arg("dt"), py::arg("dw"),
            "Evolves the process from state x0 at time t0.");

    // StochasticProcess1D ABC
    auto pyStochasticProcess1D = py::class_<StochasticProcess1D, PyStochasticProcess1D,
        ext::shared_ptr<StochasticProcess1D>, StochasticProcess>(
            base, "StochasticProcess1D",
            "Abstract base class for 1D stochastic processes.")
        .def(py::init_alias<>())
        .def("x0", &StochasticProcess1D::x0,
            "Returns the initial value.")
        .def("drift", py::overload_cast<Time, Real>(&StochasticProcess1D::drift, py::const_),
            py::arg("t"), py::arg("x"),
            "Returns the drift at time t given state x.")
        .def("diffusion", py::overload_cast<Time, Real>(&StochasticProcess1D::diffusion, py::const_),
            py::arg("t"), py::arg("x"),
            "Returns the diffusion at time t given state x.")
        .def("evolve", py::overload_cast<Time, Real, Time, Real>(&StochasticProcess1D::evolve, py::const_),
            py::arg("t0"), py::arg("x0"), py::arg("dt"), py::arg("dw"),
            "Evolves the process from state x0 at time t0.");

    // StochasticProcess1D::discretization nested ABC
    py::class_<StochasticProcess1D::discretization, PyDiscretization,
        ext::shared_ptr<StochasticProcess1D::discretization>>(
            pyStochasticProcess1D, "discretization",
            "Discretization scheme for 1D stochastic processes.")
        .def(py::init_alias<>())
        .def("drift", &StochasticProcess1D::discretization::drift,
            py::arg("process"), py::arg("t0"), py::arg("x0"), py::arg("dt"),
            "Returns the discretized drift.")
        .def("diffusion", &StochasticProcess1D::discretization::diffusion,
            py::arg("process"), py::arg("t0"), py::arg("x0"), py::arg("dt"),
            "Returns the discretized diffusion.")
        .def("variance", &StochasticProcess1D::discretization::variance,
            py::arg("process"), py::arg("t0"), py::arg("x0"), py::arg("dt"),
            "Returns the discretized variance.");
}
