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
#include <ql/cashflows/zeroinflationcashflow.hpp>
#include <ql/indexes/inflationindex.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::zeroinflationcashflow(py::module_& m) {
    py::class_<ZeroInflationCashFlow, CashFlow,
               ext::shared_ptr<ZeroInflationCashFlow>>(
        m, "ZeroInflationCashFlow",
        "Cash flow dependent on a zero-inflation index ratio.")
        .def(py::init<Real,
                       const ext::shared_ptr<ZeroInflationIndex>&,
                       CPI::InterpolationType,
                       const Date&, const Date&,
                       const Period&,
                       const Date&,
                       bool>(),
            py::arg("notional"),
            py::arg("index"),
            py::arg("observationInterpolation"),
            py::arg("startDate"),
            py::arg("endDate"),
            py::arg("observationLag"),
            py::arg("paymentDate"),
            py::arg("growthOnly") = false,
            "Constructs a zero-inflation cash flow.")
        .def("notional", &ZeroInflationCashFlow::notional,
            "Returns the notional.")
        .def("zeroInflationIndex", &ZeroInflationCashFlow::zeroInflationIndex,
            "Returns the zero-inflation index.")
        .def("observationInterpolation",
            &ZeroInflationCashFlow::observationInterpolation,
            "Returns the observation interpolation type.")
        .def("baseFixing", &ZeroInflationCashFlow::baseFixing,
            "Returns the base fixing.")
        .def("indexFixing", &ZeroInflationCashFlow::indexFixing,
            "Returns the index fixing.")
        .def("growthOnly", &ZeroInflationCashFlow::growthOnly,
            "Returns whether only growth is paid.")
        .def("baseDate", &ZeroInflationCashFlow::baseDate,
            "Returns the base date.")
        .def("fixingDate", &ZeroInflationCashFlow::fixingDate,
            "Returns the fixing date.");
}
