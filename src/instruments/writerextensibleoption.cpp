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
#include <ql/instruments/writerextensibleoption.hpp>
#include <ql/instruments/payoffs.hpp>
#include <ql/exercise.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::writerextensibleoption(py::module_& m) {
    py::class_<WriterExtensibleOption, OneAssetOption,
               ext::shared_ptr<WriterExtensibleOption>>(
        m, "WriterExtensibleOption",
        "Writer-extensible option.")
        .def(py::init<const ext::shared_ptr<PlainVanillaPayoff>&,
                      const ext::shared_ptr<Exercise>&,
                      const ext::shared_ptr<PlainVanillaPayoff>&,
                      ext::shared_ptr<Exercise>>(),
             py::arg("payoff1"),
             py::arg("exercise1"),
             py::arg("payoff2"),
             py::arg("exercise2"))
        .def("payoff2", &WriterExtensibleOption::payoff2,
             "Returns the second payoff.")
        .def("exercise2", &WriterExtensibleOption::exercise2,
             "Returns the second exercise.");
}
