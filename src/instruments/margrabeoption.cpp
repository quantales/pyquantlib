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
#include <ql/instruments/margrabeoption.hpp>
#include <ql/exercise.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::margrabeoption(py::module_& m) {
    py::class_<MargrabeOption, MultiAssetOption,
               ext::shared_ptr<MargrabeOption>>(
        m, "MargrabeOption",
        "Exchange option (Margrabe): option to exchange one asset for another.")
        .def(py::init<Integer, Integer, const ext::shared_ptr<Exercise>&>(),
             py::arg("Q1"),
             py::arg("Q2"),
             py::arg("exercise"))
        .def("delta1", &MargrabeOption::delta1,
            "Returns delta with respect to first asset.")
        .def("delta2", &MargrabeOption::delta2,
            "Returns delta with respect to second asset.")
        .def("gamma1", &MargrabeOption::gamma1,
            "Returns gamma with respect to first asset.")
        .def("gamma2", &MargrabeOption::gamma2,
            "Returns gamma with respect to second asset.");
}
