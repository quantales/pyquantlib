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
#include "pyquantlib/binding_manager.h"
#include <ql/termstructures/inflationtermstructure.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::inflationtermstructure(py::module_& m) {
    // InflationTermStructure ABC
    py::class_<InflationTermStructure, TermStructure,
               ext::shared_ptr<InflationTermStructure>>(
        m, "InflationTermStructure",
        "Abstract base class for inflation term structures.")
        .def("frequency", &InflationTermStructure::frequency,
            "Returns the frequency of the inflation index.")
        .def("baseRate", &InflationTermStructure::baseRate,
            "Returns the base rate.")
        .def("baseDate", &InflationTermStructure::baseDate,
            "Returns the base date.")
        .def("hasSeasonality", &InflationTermStructure::hasSeasonality,
            "Returns true if a seasonality correction is set.");

    // ZeroInflationTermStructure ABC
    py::class_<ZeroInflationTermStructure, InflationTermStructure,
               ext::shared_ptr<ZeroInflationTermStructure>>(
        m, "ZeroInflationTermStructure",
        "Abstract base class for zero-coupon inflation term structures.")
        .def("zeroRate",
            static_cast<Rate (ZeroInflationTermStructure::*)(
                const Date&, const Period&, bool, bool) const>(
                &ZeroInflationTermStructure::zeroRate),
            py::arg("date"),
            py::arg("instObsLag") = Period(-1, Days),
            py::arg("forceLinearInterpolation") = false,
            py::arg("extrapolate") = false,
            "Returns the zero-coupon inflation rate for the given date.");

    // YoYInflationTermStructure ABC
    py::class_<YoYInflationTermStructure, InflationTermStructure,
               ext::shared_ptr<YoYInflationTermStructure>>(
        m, "YoYInflationTermStructure",
        "Abstract base class for year-on-year inflation term structures.")
        .def("yoyRate",
            static_cast<Rate (YoYInflationTermStructure::*)(
                const Date&, const Period&, bool, bool) const>(
                &YoYInflationTermStructure::yoyRate),
            py::arg("date"),
            py::arg("instObsLag") = Period(-1, Days),
            py::arg("forceLinearInterpolation") = false,
            py::arg("extrapolate") = false,
            "Returns the year-on-year inflation rate for the given date.");
}

void ql_termstructures::zeroinflationtermstructurehandle(py::module_& m) {
    bindHandle<ZeroInflationTermStructure>(
        m, "ZeroInflationTermStructureHandle",
        "Handle to ZeroInflationTermStructure.");
    bindRelinkableHandle<ZeroInflationTermStructure>(
        m, "RelinkableZeroInflationTermStructureHandle",
        "Relinkable handle to ZeroInflationTermStructure.");

    // Free function from inflationtermstructure.hpp
    m.def("inflationPeriod", &inflationPeriod,
        py::arg("date"), py::arg("frequency"),
        "Returns the start and end dates of the inflation period.");
}

void ql_termstructures::yoyinflationtermstructurehandle(py::module_& m) {
    bindHandle<YoYInflationTermStructure>(
        m, "YoYInflationTermStructureHandle",
        "Handle to YoYInflationTermStructure.");
    bindRelinkableHandle<YoYInflationTermStructure>(
        m, "RelinkableYoYInflationTermStructureHandle",
        "Relinkable handle to YoYInflationTermStructure.");
}
