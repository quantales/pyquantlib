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
