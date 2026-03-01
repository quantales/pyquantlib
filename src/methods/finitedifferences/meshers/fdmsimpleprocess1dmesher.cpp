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
#include <ql/methods/finitedifferences/meshers/fdmsimpleprocess1dmesher.hpp>
#include <ql/stochasticprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmsimpleprocess1dmesher(py::module_& m) {
    py::class_<FdmSimpleProcess1dMesher, Fdm1dMesher,
               ext::shared_ptr<FdmSimpleProcess1dMesher>>(
        m, "FdmSimpleProcess1dMesher",
        "One-dimensional mesher for a generic stochastic process.")
        .def(py::init([](Size size,
                         const ext::shared_ptr<StochasticProcess1D>& process,
                         Time maturity, Size tAvgSteps, Real epsilon,
                         const py::object& mandatoryPoint) {
            Real mp = mandatoryPoint.is_none()
                ? Null<Real>() : mandatoryPoint.cast<Real>();
            return ext::make_shared<FdmSimpleProcess1dMesher>(
                size, process, maturity, tAvgSteps, epsilon, mp);
        }),
            py::arg("size"),
            py::arg("process"),
            py::arg("maturity"),
            py::arg("tAvgSteps") = 10,
            py::arg("epsilon") = 0.0001,
            py::arg("mandatoryPoint") = py::none(),
            "Constructs from a 1D stochastic process.");
}
