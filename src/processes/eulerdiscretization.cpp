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
#include <ql/processes/eulerdiscretization.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_processes::eulerdiscretization(py::module_& m) {
    py::class_<EulerDiscretization, StochasticProcess1D::discretization,
               ext::shared_ptr<EulerDiscretization>>(
        m, "EulerDiscretization",
        "Euler discretization for 1D stochastic processes.")
        .def(py::init<>());
}
