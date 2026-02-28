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
#include <ql/processes/forwardmeasureprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_processes::forwardmeasureprocess(py::module_& m) {
    // ForwardMeasureProcess ABC (multi-dimensional)
    py::class_<ForwardMeasureProcess, ext::shared_ptr<ForwardMeasureProcess>,
               StochasticProcess>(
        m, "ForwardMeasureProcess",
        "Forward-measure stochastic process.")
        .def("setForwardMeasureTime",
            &ForwardMeasureProcess::setForwardMeasureTime,
            py::arg("T"),
            "Sets the forward measure maturity time.")
        .def("getForwardMeasureTime",
            &ForwardMeasureProcess::getForwardMeasureTime,
            "Returns the forward measure maturity time.");

    // ForwardMeasureProcess1D ABC (one-dimensional)
    py::class_<ForwardMeasureProcess1D, ext::shared_ptr<ForwardMeasureProcess1D>,
               StochasticProcess1D>(
        m, "ForwardMeasureProcess1D",
        "Forward-measure 1-D stochastic process.")
        .def("setForwardMeasureTime",
            &ForwardMeasureProcess1D::setForwardMeasureTime,
            py::arg("T"),
            "Sets the forward measure maturity time.")
        .def("getForwardMeasureTime",
            &ForwardMeasureProcess1D::getForwardMeasureTime,
            "Returns the forward measure maturity time.");
}
