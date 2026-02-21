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
#include <ql/instruments/varianceswap.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::varianceswap(py::module_& m) {
    py::class_<VarianceSwap, Instrument, ext::shared_ptr<VarianceSwap>>(
        m, "VarianceSwap",
        "Variance swap instrument.")
        .def(py::init<Position::Type, Real, Real, const Date&, const Date&>(),
            py::arg("position"),
            py::arg("strike"),
            py::arg("notional"),
            py::arg("startDate"),
            py::arg("maturityDate"),
            "Constructs a variance swap.")
        .def("strike", &VarianceSwap::strike,
            "Returns the variance strike.")
        .def("position", &VarianceSwap::position,
            "Returns the position type.")
        .def("startDate", &VarianceSwap::startDate,
            "Returns the start date.")
        .def("maturityDate", &VarianceSwap::maturityDate,
            "Returns the maturity date.")
        .def("notional", &VarianceSwap::notional,
            "Returns the notional.")
        .def("variance", &VarianceSwap::variance,
            "Returns the realized variance.");
}
