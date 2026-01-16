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
#include <ql/models/equity/piecewisetimedependenthestonmodel.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::piecewisetimedependenthestonmodel(py::module_& m) {
    py::class_<PiecewiseTimeDependentHestonModel, CalibratedModel,
               ext::shared_ptr<PiecewiseTimeDependentHestonModel>>(
        m, "PiecewiseTimeDependentHestonModel",
        "Piecewise time-dependent Heston stochastic volatility model.")
        .def(py::init<const Handle<YieldTermStructure>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<Quote>&,
                      Real,
                      const Parameter&,
                      const Parameter&,
                      const Parameter&,
                      const Parameter&,
                      const TimeGrid&>(),
             py::arg("riskFreeRate"), py::arg("dividendYield"), py::arg("s0"),
             py::arg("v0"), py::arg("theta"), py::arg("kappa"),
             py::arg("sigma"), py::arg("rho"), py::arg("timeGrid"),
            "Constructs time-dependent Heston model.")
        .def("theta", &PiecewiseTimeDependentHestonModel::theta,
            py::arg("t"),
            "Returns theta at time t.")
        .def("kappa", &PiecewiseTimeDependentHestonModel::kappa,
            py::arg("t"),
            "Returns kappa at time t.")
        .def("sigma", &PiecewiseTimeDependentHestonModel::sigma,
            py::arg("t"),
            "Returns sigma at time t.")
        .def("rho", &PiecewiseTimeDependentHestonModel::rho,
            py::arg("t"),
            "Returns rho at time t.")
        .def("v0", &PiecewiseTimeDependentHestonModel::v0,
            "Returns initial variance.")
        .def("s0", &PiecewiseTimeDependentHestonModel::s0,
            "Returns initial spot price.")
        .def("timeGrid", &PiecewiseTimeDependentHestonModel::timeGrid,
            "Returns the time grid.")
        .def("dividendYield", &PiecewiseTimeDependentHestonModel::dividendYield,
            "Returns dividend yield term structure.")
        .def("riskFreeRate", &PiecewiseTimeDependentHestonModel::riskFreeRate,
            "Returns risk-free rate term structure.");
}
