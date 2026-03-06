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
#include <ql/experimental/finitedifferences/glued1dmesher.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::glued1dmesher(py::module_& m) {
    py::class_<Glued1dMesher, Fdm1dMesher,
               ext::shared_ptr<Glued1dMesher>>(
        m, "Glued1dMesher",
        "Combines two 1D meshers into one by gluing at their boundary.")
        .def(py::init<const Fdm1dMesher&, const Fdm1dMesher&>(),
            py::arg("leftMesher"), py::arg("rightMesher"),
            "Constructs by gluing left and right meshers.");
}
