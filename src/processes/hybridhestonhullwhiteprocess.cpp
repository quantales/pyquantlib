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
#include <ql/processes/hybridhestonhullwhiteprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_processes::hybridhestonhullwhiteprocess(py::module_& m) {
    auto cls = py::class_<HybridHestonHullWhiteProcess, StochasticProcess,
                          ext::shared_ptr<HybridHestonHullWhiteProcess>>(
        m, "HybridHestonHullWhiteProcess",
        "Hybrid Heston Hull-White three-factor stochastic process.");

    py::enum_<HybridHestonHullWhiteProcess::Discretization>(cls, "Discretization",
        "Discretization schemes for hybrid process.")
        .value("Euler", HybridHestonHullWhiteProcess::Euler)
        .value("BSMHullWhite", HybridHestonHullWhiteProcess::BSMHullWhite)
        .export_values();

    cls.def(py::init<const ext::shared_ptr<HestonProcess>&,
                     const ext::shared_ptr<HullWhiteForwardProcess>&,
                     Real,
                     HybridHestonHullWhiteProcess::Discretization>(),
            py::arg("hestonProcess"),
            py::arg("hullWhiteProcess"),
            py::arg("corrEquityShortRate"),
            py::arg("discretization") = HybridHestonHullWhiteProcess::BSMHullWhite,
            "Constructs HybridHestonHullWhiteProcess.")
        .def("hestonProcess", &HybridHestonHullWhiteProcess::hestonProcess,
            py::return_value_policy::reference_internal,
            "Returns the Heston process.")
        .def("hullWhiteProcess", &HybridHestonHullWhiteProcess::hullWhiteProcess,
            py::return_value_policy::reference_internal,
            "Returns the Hull-White forward process.")
        .def("eta", &HybridHestonHullWhiteProcess::eta,
            "Returns the equity-rate correlation.")
        .def("discretization", &HybridHestonHullWhiteProcess::discretization,
            "Returns the discretization scheme.");
}
